# 🚀 Video Transcription Pro - Installation Guide

Choose the installation method that best fits your needs:

---

## 📋 Quick Installation Guide

| Method | Best For | Complexity | GPU Support |
|--------|----------|------------|-------------|
| [🐳 Docker](#-docker-installation) | **Everyone** - Easiest | ⭐ | ✅ Yes |
| [🚀 uv](#-uv-installation) | **Developers** - Modern | ⭐⭐ | ✅ Yes |
| [📦 pip](#-pip-installation) | **Traditional** - Fallback | ⭐⭐⭐ | ✅ Yes |

---

# 🐳 Docker Installation (Recommended)

**Works on Windows, Linux, macOS - No dependencies to install!**

## Quick Start
```bash
# CPU version (works everywhere)
docker run --rm -v "$(pwd):/app" videotranscriptionpro/video-transcription-pro:latest-cpu your_video.mp4

# GPU version (Linux/Windows WSL2)
docker run --rm --gpus all -v "$(pwd):/app" videotranscriptionpro/video-transcription-pro:latest-gpu your_video.mp4
```

## Step-by-Step

### 1. Install Docker
- **Windows/macOS**: Download [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Linux**: Follow [Docker installation guide](https://docs.docker.com/engine/install/)

### 2. Test Installation
```bash
# Test CPU version
docker run --rm videotranscriptionpro/video-transcription-pro:latest-cpu --help

# Test GPU version (if you have NVIDIA GPU)
docker run --rm --gpus all videotranscriptionpro/video-transcription-pro:latest-gpu --help
```

### 3. Transcribe Your First Video
```bash
# Basic transcription
docker run --rm -v "$(pwd):/app" videotranscriptionpro/video-transcription-pro:latest-cpu your_video.mp4

# With custom output
docker run --rm \
  -v "$(pwd)/videos:/app/videos:ro" \
  -v "$(pwd)/transcripts:/app/transcripts" \
  videotranscriptionpro/video-transcription-pro:latest-cpu \
  /app/videos/your_video.mp4 -o /app/transcripts
```

---

# 🚀 uv Installation (Modern Python)

**Fast, reliable dependency management for Python developers**

## Quick Start
```bash
# Install uv
pip install uv

# Install with GPU support
uv pip install video-transcription-pro[gpu]
```

## Step-by-Step

### 1. Install uv
```bash
# Using pip
pip install uv

# Or using curl (Linux/macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Create Environment and Install
```bash
# Create virtual environment
uv venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install with GPU support
uv pip install video-transcription-pro[gpu]
```

### 3. Verify Installation
```bash
python -c "import video_transcription; print('✅ Installation successful!')"
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

---

# 📦 pip Installation (Traditional)

**Standard Python package installation**

## Quick Start
```bash
# CPU only
pip install video-transcription-pro

# With GPU support
pip install video-transcription-pro[gpu]
```

## Step-by-Step

### 1. Install Python Dependencies
```bash
# Install PyTorch with CUDA (if you have GPU)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install the package
pip install video-transcription-pro[gpu]
```

### 2. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
```bash
# Download from https://ffmpeg.org/download.html
# Or use chocolatey: choco install ffmpeg
```

### 3. Test Installation
```bash
python -c "import video_transcription; print('✅ Installation successful!')"
```

---

# 🔧 Platform-Specific Notes

## Windows
- **Recommended**: Docker or uv
- **Alternative**: Use WSL2 for better Linux compatibility
- **GPU**: Requires NVIDIA drivers and CUDA toolkit

## Linux
- **Recommended**: Docker or uv
- **GPU**: Works best with NVIDIA drivers
- **System**: Ubuntu 20.04+ recommended

## macOS
- **Recommended**: Docker
- **GPU**: Limited GPU support (M1/M2 chips work with CPU)
- **Alternative**: uv works well on macOS

---

# 🐛 Troubleshooting

## Common Issues

### Docker Issues
```bash
# Permission denied
sudo usermod -aG docker $USER

# GPU not detected
nvidia-smi  # Check if NVIDIA drivers are installed
```

### uv Issues
```bash
# Clear cache
uv cache clean

# Reinstall
uv pip uninstall video-transcription-pro
uv pip install video-transcription-pro[gpu]
```

### pip Issues
```bash
# Upgrade pip
pip install --upgrade pip

# Install in virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
pip install video-transcription-pro[gpu]
```

## Getting Help
- 📖 [Documentation](https://video-transcription-pro.readthedocs.io/)
- 🐛 [GitHub Issues](https://github.com/yourusername/video-transcription-pro/issues)
- 💬 [Discussions](https://github.com/yourusername/video-transcription-pro/discussions)

---

**🎉 Ready to transcribe! Start with Docker for the easiest experience.**
