import streamlit as st
import subprocess
import os
import tempfile
import requests
import re
from typing import Tuple
import os
import shutil
import signal
import subprocess
from pathlib import Path

# --------- CONFIG ---------
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "deepseek/deepseek-chat-v3-0324:free"

# --------- ENHANCED FUNCTIONS ---------

def call_openrouter(prompt: str) -> dict:
    """Call OpenRouter API with improved error handling."""
    headers = {
        "Authorization": f"Bearer {st.session_state.openrouter_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a world-class Manim CE expert. Your task is to generate EXCLUSIVELY valid Python code for Manim CE animations.\n"
                    "STRICT RULES:\n"
                    "1. ONLY output code between ```python and ``` delimiters\n"
                    "2. NO natural language explanations\n"
                    "3. Use ONLY Text() for text elements\n"
                    "4. Include necessary imports (manim, numpy, math)\n"
                    "5. Class must inherit from Scene\n"
                    "EXAMPLE:\n"
                    "```python\n"
                    "from manim import *\n\n"
                    "class DemoScene(Scene):\n"
                    "    def construct(self):\n"
                    "        # Your animation code\n"
                    "```"
                )
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 1000
    }

    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def call_openrouter_edit(current_code: str, changes: str) -> dict:
    """Call OpenRouter API specifically for editing existing code."""
    headers = {
        "Authorization": f"Bearer {st.session_state.openrouter_api_key}",
        "Content-Type": "application/json"
    }

    edit_prompt = f"""Code of current animation:

{current_code}

Requested changes:

{changes}

Modify the existing code to implement the requested changes. ONLY output the complete modified code between ```python and ``` delimiters with NO explanations."""

    data = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a world-class Manim CE expert. Your task is to modify existing Manim CE code based on user requests.\n"
                    "STRICT RULES:\n"
                    "1. ONLY output the complete modified code between ```python and ``` delimiters\n"
                    "2. NO natural language explanations\n"
                    "3. Keep the same class structure\n"
                    "4. Implement the requested changes precisely\n"
                    "5. Maintain code quality and syntax\n"
                )
            },
            {"role": "user", "content": edit_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 1200
    }

    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def extract_code_only(text: str) -> str:
    """Robust code extraction with multiple fallback strategies."""
    # Strategy 1: Extract code blocks
    code_blocks = re.findall(r"```python(.*?)```", text, re.DOTALL)
    if not code_blocks:
        code_blocks = re.findall(r"```(.*?)```", text, re.DOTALL)
    
    if code_blocks:
        code = max(code_blocks, key=len).strip()
        # Remove residual backticks and non-code lines
        code = re.sub(r"^`+", "", code, flags=re.MULTILINE)
        code = re.sub(r"`+$", "", code, flags=re.MULTILINE)
        return code
    
    # Strategy 2: Find code-like patterns
    code_start = re.search(r"^(from|import|class)\b", text, re.MULTILINE)
    if code_start:
        return text[code_start.start():]
    
    # Final fallback: Remove non-code lines
    return "\n".join([line for line in text.split("\n") if re.match(r"^\s*(from|import|class|def)", line)])

def save_code_to_file(code: str, folder: str) -> str:
    """Save code with validation."""
    path = os.path.join(folder, "scene.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write("from manim import *\n")  # Ensure base import
        f.write(code)
    return path

def get_manim_path():
    """Detect Manim path for different environments"""
    # Try to find manim executable
    manim_path = shutil.which('manim')
    if manim_path:
        return manim_path
    
    # Fallback paths for different environments
    possible_paths = [
        '/usr/local/bin/manim',  # Docker container
        '/opt/conda/bin/manim',  # Conda environment
        '/home/manimuser/.local/bin/manim',  # Manim Docker image default
        'manim'  # System PATH
    ]
    
    for path in possible_paths:
        if shutil.which(path) or os.path.exists(path):
            return path
    
    return 'manim'  # Default fallback

def render_with_timeout(command, timeout=300):
    """Execute manim command with timeout and better error handling"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout,
            cwd=os.getcwd()
        )
        return result
    except subprocess.TimeoutExpired:
        st.error("⏰ Animation rendering timed out (5 minutes). Try a simpler animation.")
        return None
    except Exception as e:
        st.error(f"❌ Error during rendering: {str(e)}")
        return None

def execute_manim_render(temp_file, class_name, video_path):
    """Execute manim rendering with cloud-optimized settings"""
    MANIM_PATH = get_manim_path()
    render_command = f"{MANIM_PATH} -pql {temp_file} {class_name} --output_file {video_path}"
    
    st.info("🎬 Rendering animation... (this may take 1-2 minutes)")
    result = render_with_timeout(render_command, timeout=300)
    
    if result is None:
        return False
        
    if result.returncode != 0:
        st.error(f"❌ Rendering failed: {result.stderr}")
        st.info("🔄 Trying alternative rendering settings...")
        alt_command = f"{MANIM_PATH} --resolution 480,320 --fps 15 {temp_file} {class_name} --output_file {video_path}"
        alt_result = render_with_timeout(alt_command, timeout=300)
        if alt_result and alt_result.returncode == 0:
            return True
        return False
    
    return True


def run_manim(scene_file: str, scene_name: str, output_dir: str) -> Tuple[bool, str]:
    """Run Manim with enhanced error handling."""
    MANIM_PATH = get_manim_path() # Replace with your Manim path 
    cmd = [
        MANIM_PATH,
        "-ql",
        scene_file,
        scene_name,
        "--media_dir", output_dir,
        "--output_file", scene_name
    ]
    
    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            cwd=output_dir,
            timeout=120
        )
        
        # Find output video
        video_dir = os.path.join(output_dir, "videos", "scene", "480p15")
        for file in os.listdir(video_dir):
            if file.endswith(".mp4") and scene_name in file:
                return True, os.path.join(video_dir, file)
        
        return False, "Video file not found"
        
    except subprocess.CalledProcessError as e:
        error_msg = f"{e.stderr}\n\nPossible solutions:\n1. Check code syntax\n2. Verify FFmpeg installation\n3. Ensure proper class definition"
        return False, error_msg
    except Exception as e:
        return False, str(e)

def get_api_key():
    """Get API key from environment or user input"""
    api_key = os.environ.get('OPENROUTER_API_KEY', '')
    if api_key:
        return api_key
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    with st.sidebar:
        st.markdown("### 🔑 API Configuration")
        api_key = st.text_input(
            "OpenRouter API Key",
            value=st.session_state.api_key,
            type="password",
            help="Get your API key from https://openrouter.ai/keys"
        )
        st.session_state.api_key = api_key
    return api_key

# --------- STREAMLIT UI ENHANCEMENTS ---------

st.set_page_config(page_title="Cursor for 2D Animator", layout="wide")
st.markdown("""
    <style>
    .stTextArea textarea {font-family: monospace !important;}
    .stAlert {padding: 20px !important;}
    .edit-mode {
        background-color: #1e3a8a;
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if "history" not in st.session_state:
    st.session_state.history = []
if "openrouter_api_key" not in st.session_state:
    st.session_state.openrouter_api_key = ""
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "current_animation" not in st.session_state:
    st.session_state.current_animation = None

# Create persistent media directory
os.makedirs("persistent_media", exist_ok=True)

# UI Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Prompt Interface")
    
    # API Key Input
    st.text_input(
        "OpenRouter API Key",
        type="password",
        key="openrouter_api_key",
        help="Get your API key from https://openrouter.ai/keys"
    )
    
    # Show current mode
    if st.session_state.edit_mode and st.session_state.current_animation:
        st.markdown('<div class="edit-mode">🔧 EDIT MODE: Modifying current animation</div>', unsafe_allow_html=True)
        
        # Show current animation info
        st.info(f"Current Animation: {st.session_state.current_animation.get('prompt', 'Unknown')[:100]}...")
        
        # Edit interface
        edit_prompt = st.text_area(
            "Describe the changes you want to make:",
            height=150,
            placeholder="e.g., 'Change the color to red', 'Make it rotate slower', 'Add a second square'"
        )
        
        col_edit1, col_edit2 = st.columns(2)
        
        with col_edit1:
            if st.button("Apply Changes", use_container_width=True):
                if not st.session_state.openrouter_api_key.strip():
                    st.error("Please enter your OpenRouter API key")
                elif not edit_prompt.strip():
                    st.error("Please describe the changes you want to make")
                else:
                    with st.spinner("Applying changes (may take 1-2 minutes)..."):
                        # Get current code
                        current_code = st.session_state.current_animation["code"]
                        
                        # API Call for editing
                        response = call_openrouter_edit(current_code, edit_prompt.strip())
                        
                        if "error" in response:
                            st.error(f"API Error: {response['error']}")
                        else:
                            # Process response
                            raw_code = response.get("choices", [{}])[0].get("message", {}).get("content", "")
                            clean_code = extract_code_only(raw_code)
                            
                            if not clean_code:
                                st.error("No valid code generated")
                            else:
                                # Execute Manim
                                with tempfile.TemporaryDirectory() as tmpdir:
                                    scene_path = save_code_to_file(clean_code, tmpdir)
                                    scene_match = re.search(r"class\s+(\w+)\(Scene\):", clean_code)
                                    scene_name = scene_match.group(1) if scene_match else "GeneratedScene"
                                    
                                    success, result = run_manim("scene.py", scene_name, tmpdir)
                                    
                                    # Update current animation
                                    if success:
                                        try:
                                            with open(result, "rb") as f:
                                                video_data = f.read()
                                            
                                            # Update current animation
                                            st.session_state.current_animation = {
                                                "prompt": f"EDITED: {edit_prompt}",
                                                "code": clean_code,
                                                "error": None,
                                                "video": video_data,
                                                "original_prompt": st.session_state.current_animation.get("original_prompt", st.session_state.current_animation["prompt"])
                                            }
                                            
                                            # Add to history
                                            st.session_state.history.append(st.session_state.current_animation.copy())
                                            st.rerun()
                                            
                                        except Exception as e:
                                            st.error(f"Video read error: {str(e)}")
                                    else:
                                        st.error(f"Execution Error:\n{result}")
        
        with col_edit2:
            if st.button("Cancel Edit", use_container_width=True):
                st.session_state.edit_mode = False
                st.rerun()
    
    else:
        # Normal creation mode
        new_prompt = st.text_area("Animation Description", height=150,
                                 placeholder="Describe your animation (e.g., 'Create a rotating square with velocity vectors')")
        
        if st.button("Generate Animation", use_container_width=True):
            if not st.session_state.openrouter_api_key.strip():
                st.error("Please enter your OpenRouter API key")
            else:
                with st.spinner("Generating (may take 1-2 minutes)..."):
                    # API Call
                    response = call_openrouter(new_prompt.strip())
                    
                    if "error" in response:
                        st.error(f"API Error: {response['error']}")
                    else:
                        # Process response
                        raw_code = response.get("choices", [{}])[0].get("message", {}).get("content", "")
                        clean_code = extract_code_only(raw_code)
                        
                        if not clean_code:
                            st.error("No valid code generated")
                        else:
                            # Execute Manim
                            with tempfile.TemporaryDirectory() as tmpdir:
                                scene_path = save_code_to_file(clean_code, tmpdir)
                                scene_match = re.search(r"class\s+(\w+)\(Scene\):", clean_code)
                                scene_name = scene_match.group(1) if scene_match else "GeneratedScene"
                                
                                success, result = run_manim("scene.py", scene_name, tmpdir)
                                
                                # Store results
                                entry = {
                                    "prompt": new_prompt,
                                    "code": clean_code,
                                    "error": None,
                                    "video": None,
                                    "original_prompt": new_prompt
                                }
                                
                                if success:
                                    try:
                                        with open(result, "rb") as f:
                                            entry["video"] = f.read()
                                    except Exception as e:
                                        entry["error"] = f"Video read error: {str(e)}"
                                else:
                                    entry["error"] = result
                                    
                                st.session_state.history.append(entry)
                                st.session_state.current_animation = entry
                                st.rerun()

with col2:
    st.header("Results")
    
    if st.session_state.history:
        latest = st.session_state.history[-1]
        
        if latest["error"]:
            st.error(f"Execution Error:\n{latest['error']}")
        else:
            st.success("Animation Generated Successfully!")
            st.video(latest["video"])
            st.download_button(
                "Download MP4",
                data=latest["video"],
                file_name="animation.mp4",
                mime="video/mp4"
            )
        
        with st.expander("Generated Code"):
            st.code(latest["code"], language="python")
        
        # Action buttons after successful generation
        if not latest["error"]:
            st.markdown("---")
            st.subheader("What would you like to do next?")
            
            col_action1, col_action2 = st.columns(2)
            
            with col_action1:
                if st.button("🎬 Create New Animation", use_container_width=True):
                    st.session_state.edit_mode = False
                    st.session_state.current_animation = None
                    st.rerun()
            
            with col_action2:
                if st.button("✏️ Edit Current Animation", use_container_width=True):
                    st.session_state.edit_mode = True
                    st.session_state.current_animation = latest
                    st.rerun()
            
    st.markdown("---")
    st.write("Troubleshooting Guide:")
    st.markdown("""
    1. Ensure descriptions are clear and specific
    2. Avoid complex physics simulations
    3. Use simple geometric shapes
    4. Mention color preferences explicitly
    """)

# History Management
if st.session_state.history:
    with st.sidebar:
        st.header("History")
        for idx, entry in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Animation #{len(st.session_state.history)-idx}"):
                st.write(entry.get("original_prompt", entry["prompt"]))
                if "EDITED:" in entry["prompt"]:
                    st.caption(f"Last edit: {entry['prompt']}")
                if entry["video"]:
                    st.video(entry["video"])
                    if st.button(f"Edit This Animation", key=f"edit_{idx}"):
                        st.session_state.edit_mode = True
                        st.session_state.current_animation = entry
                        st.rerun()
                if entry["error"]:
                    st.error(entry["error"])