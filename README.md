# Cursor for 2D Animator 🎬

<div align="center">
  <img src="gif/0529.gif" alt="Cursor 2D Animator Demo" width="800"/>
  <p><em>Transform natural language into beautiful mathematical animations</em></p>
</div>

A powerful Streamlit application that generates mathematical animations using natural language descriptions. Powered by OpenRouter AI and Manim Community Edition, this tool transforms your text descriptions into beautiful 2D animations with code generation and editing capabilities.

## 🌟 Features

### Core Functionality
- **Natural Language to Animation**: Describe your animation in plain English and get a working Manim animation
- **Real-time Code Generation**: AI generates clean, executable Manim CE Python code
- **Interactive Animation Editing**: Modify existing animations with simple text instructions
- **Live Preview**: Instant video preview of generated animations
- **Code Inspection**: View and analyze the generated Python code
- **Animation History**: Keep track of all your created animations
- **Download Support**: Export animations as MP4 files

### Advanced Features
- **Edit Mode**: Iteratively improve animations without starting from scratch
- **Error Handling**: Comprehensive error reporting with suggested solutions
- **Robust Code Extraction**: Multiple fallback strategies for code parsing
- **Session Management**: Persistent animation history during your session
- **Professional UI**: Clean, modern interface with syntax highlighting

## 🎯 Use Cases

- **Educational Content**: Create mathematical visualizations for teaching
- **Presentations**: Generate custom animations for slides and demos
- **Learning Manim**: Understand Manim syntax through AI-generated examples
- **Rapid Prototyping**: Quickly test animation concepts
- **Content Creation**: Produce animations for videos, tutorials, or social media

## 🚀 Live Demo

<div align="center">
  <img src="gif/0529.gif" alt="Application Demo" width="700"/>
  <p><em>Watch the app in action - from text description to animated video</em></p>
</div>

## 🎨 Key Features Showcase

<img src="gif/0529.gif" alt="Natural Language Animation" width="400" align="right"/>

### ✨ Natural Language to Animation
Simply describe what you want to animate in plain English, and watch as our AI generates beautiful Manim animations automatically.

### ⚡ Real-time Code Generation  
AI generates clean, executable Manim CE Python code that you can view, modify, and learn from.

### 🔧 Interactive Edit Mode
Modify existing animations with simple text instructions - no coding required!

<br clear="right"/>

## 🚀 Quick Start

### Prerequisites

Before setting up the project, ensure you have:
- Python 3.8 or higher
- Git (for cloning the repository)
- FFmpeg (required by Manim)
- At least 2GB of free disk space

### Installation Guide

#### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/cursor-2d-animator.git
cd cursor-2d-animator
```

#### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
# Install required packages
pip install streamlit requests manim

# For additional dependencies
pip install numpy matplotlib pillow
```

#### Step 4: Install FFmpeg

**Windows:**
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your system PATH
4. Verify installation: `ffmpeg -version`

**macOS:**
```bash
# Using Homebrew
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Step 5: Configure Manim Path
Update the `MANIM_PATH` variable in the code to match your installation:
```python
# In the code, line ~89
MANIM_PATH = r"path/to/your/manim/installation"
```

To find your Manim path:
```bash
# In your activated virtual environment
which manim
# or
where manim
```

## 🔑 Getting OpenRouter API Key

### Step 1: Create Account
1. Visit [OpenRouter.ai](https://openrouter.ai)
2. Click "Sign Up" or "Get Started"
3. Create account using email or OAuth providers (Google, GitHub, etc.)

### Step 2: Access API Keys
1. After logging in, navigate to [API Keys](https://openrouter.ai/keys)
2. Click "Create Key" or "New API Key"
3. Give your key a descriptive name (e.g., "Cursor 2D Animator")
4. Set usage limits if desired (optional)
5. Click "Create Key"

### Step 3: Copy and Secure Your Key
1. **Copy the API key immediately** (it won't be shown again)
2. Store it securely - never commit it to version control
3. The key format looks like: `sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 4: Add Credits (If Needed)
1. Go to [Billing](https://openrouter.ai/activity) in your OpenRouter dashboard
2. Most models have free tiers, but you may want to add credits for higher usage
3. The app uses `deepseek/deepseek-chat-v3-0324:free` model by default (free tier)

### API Key Security Tips
- Never share your API key publicly
- Use environment variables in production
- Consider creating separate keys for different projects
- Monitor your usage in the OpenRouter dashboard

## 🖥️ Running the Application

### Start the Application
```bash
# Make sure your virtual environment is activated
streamlit run app.py
```

### Access the Interface
1. Open your browser to `http://localhost:8501`
2. Enter your OpenRouter API key in the provided field
3. Start creating animations!

### First Animation
Try this example prompt:
```
Create a blue circle that moves in a figure-8 pattern while changing colors from blue to red
```

<div align="center">
  <img src="gif/0529.gif" alt="Example Animation Output" width="500"/>
  <p><em>Example of generated animation from natural language description</em></p>
</div>

## 📖 Usage Guide

### Creating Your First Animation

<div align="center">
  <img src="gif/0529.gif" alt="Step by Step Process" width="600"/>
  <p><em>Complete workflow: Describe → Generate → Download</em></p>
</div>

1. **Enter API Key**: Input your OpenRouter API key (required for first use)
2. **Describe Animation**: Write a clear description of what you want to animate
3. **Generate**: Click "Generate Animation" and wait 1-2 minutes
4. **Review**: View the generated video and code
5. **Download**: Save the MP4 file if satisfied

### Example Prompts

**Basic Shapes:**
```
Create a red square that rotates 360 degrees clockwise
```

**Mathematical Concepts:**
```
Show a sine wave function being drawn from left to right with a moving dot
```

**Complex Animations:**
```
Create two circles orbiting around a central point with different speeds and colors
```

**Text Animations:**
```
Display the text "Hello Manim" with each letter appearing one by one
```

### Editing Existing Animations

<img src="gif/0529.gif" alt="Edit Mode Demo" width="450" align="left"/>

1. **Generate Initial Animation**: Create your base animation first
2. **Enter Edit Mode**: Click "✏️ Edit Current Animation"  
3. **Describe Changes**: Specify what you want to modify
4. **Apply Changes**: The AI will modify the existing code
5. **Iterate**: Continue editing until satisfied

<br clear="left"/>

### Example Animation Prompts

**Basic Shapes:**
```
Create a red square that rotates 360 degrees clockwise
```

**Mathematical Concepts:**
```
Show a sine wave function being drawn from left to right with a moving dot
```

**Complex Animations:**
```
Create two circles orbiting around a central point with different speeds and colors
```

**Text Animations:**
```
Display the text "Hello Manim" with each letter appearing one by one
```

## 🔧 Configuration Options

### Streamlit Configuration
The `.streamlit/config.toml` file contains app-specific settings:
```toml
[theme]
primaryColor = "#ff6b6b"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
maxUploadSize = 200
```

### Model Configuration
You can change the AI model by modifying:
```python
MODEL_NAME = "deepseek/deepseek-chat-v3-0324:free"
```

Available free models:
- `deepseek/deepseek-chat-v3-0324:free`
- `google/gemini-flash-1.5:free`
- `meta-llama/llama-3.1-8b-instruct:free`

### Output Quality
Modify Manim render settings:
```python
# Change -ql to other quality settings:
# -ql: Low quality (480p, fast)
# -qm: Medium quality (720p)
# -qh: High quality (1080p)
# -qk: 4K quality (slow)
```

### Media Storage
Generated animations are automatically saved in the `persistent_media/` directory for future reference and download.

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. "Manim not found" Error
**Problem**: System can't locate Manim executable
**Solution**: 
- Verify Manim installation: `manim --version`
- Update `MANIM_PATH` in the code
- Ensure virtual environment is activated

#### 2. FFmpeg Issues
**Problem**: Video encoding fails
**Solutions**:
- Install FFmpeg properly
- Add FFmpeg to system PATH
- Restart terminal/command prompt after installation

#### 3. API Key Errors
**Problem**: Authentication failures
**Solutions**:
- Verify API key is correct and active
- Check OpenRouter account status
- Ensure no extra spaces in the key

#### 4. Code Generation Issues
**Problem**: Generated code doesn't work
**Solutions**:
- Use more specific descriptions
- Avoid overly complex requests
- Check the generated code for syntax errors

#### 5. Import Errors
**Problem**: Missing Python packages
**Solution**:
```bash
pip install --upgrade streamlit requests manim numpy matplotlib
```

#### 6. Memory Issues
**Problem**: Application crashes with large animations
**Solutions**:
- Use lower quality settings (-ql)
- Avoid complex animations with many objects
- Restart the application periodically

### Error Messages Reference

| Error | Cause | Solution |
|-------|-------|----------|
| "No valid code generated" | AI didn't produce parseable code | Rephrase your prompt more clearly |
| "Video file not found" | Manim execution failed | Check Manim installation and code syntax |
| "API Error: 401" | Invalid API key | Verify OpenRouter API key |
| "Timeout Error" | Operation took too long | Simplify animation or increase timeout |

## 📁 Project Structure

```
cursor-2d-animator/
├── app.py                    # Main Streamlit application
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── gif/
│   └── 0529.gif            # Demo animations and screenshots
└── persistent_media/        # Generated animations storage
```

## 🎨 Animation Examples

### Basic Geometric Shapes
```python
from manim import *

class RotatingSquare(Scene):
    def construct(self):
        square = Square(color=BLUE)
        self.play(Rotate(square, TAU), run_time=3)
```

### Mathematical Functions  
```python
from manim import *

class SineWave(Scene):
    def construct(self):
        axes = Axes()
        sine_curve = axes.plot(lambda x: np.sin(x), color=YELLOW)
        self.play(Create(axes), Create(sine_curve))
```

### Text Animations
```python
from manim import *

class TextExample(Scene):
    def construct(self):
        text = Text("Hello Manim!", font_size=48)
        self.play(Write(text))
        self.play(text.animate.set_color(RED))
```

<div align="center">
  <img src="gif/0529.gif" alt="Generated Animation Examples" width="600"/>
  <p><em>Various types of animations you can create with natural language descriptions</em></p>
</div>

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Reporting Issues
1. Check existing issues first
2. Use the issue template
3. Provide detailed reproduction steps
4. Include error messages and screenshots

### Feature Requests
1. Describe the feature clearly
2. Explain the use case
3. Consider backward compatibility

### Code Contributions
1. Fork the repository
2. Create a feature branch
3. Follow PEP 8 style guidelines
4. Add tests for new features
5. Update documentation
6. Submit a pull request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/cursor-2d-animator.git

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run linting
flake8 app.py
black app.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Manim Community Edition** - The powerful animation engine
- **OpenRouter** - AI model access and management
- **Streamlit** - Beautiful web app framework
- **DeepSeek** - Default AI model for code generation

## 📞 Support

### Getting Help
- **Documentation**: Check this README and inline comments
- **Issues**: Open a GitHub issue for bugs
- **Discussions**: Use GitHub Discussions for questions
- **Community**: Join the Manim Discord server

### Useful Links
- [Manim Documentation](https://docs.manim.community/)
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [FFmpeg Download](https://ffmpeg.org/download.html)

## 🔄 Version History

### v1.0.0 (Current)
- Initial release
- Basic animation generation
- Edit mode functionality
- History management
- Error handling and troubleshooting

### Planned Features
- Animation templates library
- Batch processing
- Custom model support
- Advanced editing tools
- Animation sharing
- Mobile responsiveness

---

**Happy Animating! 🎬✨**

> *Transform your ideas into beautiful mathematical animations with the power of AI and Manim.*