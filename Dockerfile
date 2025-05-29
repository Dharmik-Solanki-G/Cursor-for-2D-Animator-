# Use the official Manim Community Docker image as base
FROM manimcommunity/manim:latest

# Set working directory
WORKDIR /app

# Update package lists and install system dependencies
USER root
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Switch back to manimuser (the default user in manim image)
USER manimuser

# Install Python dependencies
RUN pip install --no-cache-dir \
    streamlit==1.29.0 \
    requests \
    pillow \
    numpy \
    matplotlib

# Copy application files
COPY --chown=manimuser:manimuser . .

# Create directories for media output
RUN mkdir -p persistent_media && \
    chmod 755 persistent_media

# Create .streamlit directory if it doesn't exist
RUN mkdir -p .streamlit

# Set the correct PATH to include local bin directory
ENV PATH="/home/manimuser/.local/bin:$PATH"

# Expose Streamlit port
EXPOSE 8501

# Set environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Command to run the application - using python -m for more reliable execution
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]