# 🚀 Video Transcription Pro - Installation Guide

Choose the installation method that best fits your environment and platform:

---

## 📋 Quick Platform Selection

| Platform | Best For | Complexity | GPU Support |
|----------|----------|------------|-------------|
| [🪟 Windows](#-windows-installation) | Windows users, development | Medium | ✅ Yes |
| [🐧 Linux](#-linux-installation) | Linux users, servers | Easy | ✅ Yes |
| [🐳 Docker](#-docker-installation) | Any platform, isolated environment | Easiest | ✅ Yes |

---

# 🪟 Windows Installation

## Prerequisites
- Windows 10/11 (64-bit)
- 8GB+ RAM (16GB+ recommended for large files)
- Optional: NVIDIA GPU with CUDA support

## Method 1: Conda (Recommended for Windows)

### 1. Install Miniconda
```powershell
# Download from: https://docs.conda.io/en/latest/miniconda.html
# Choose: Miniconda3 Windows 64-bit
# Install with default settings
```

### 2. Create Environment
```powershell
# Open Anaconda Prompt (search "Anaconda Prompt" in Start Menu)
conda create -n video-transcription-new python=3.11
conda activate video-transcription-new
```

### 3. Install PyTorch with CUDA (for GPU acceleration)
```powershell
# For NVIDIA GPU (recommended):
conda install pytorch pytorch-cuda=11.8 -c pytorch -c nvidia

# For CPU only:
conda install pytorch cpuonly -c pytorch
```

### 4. Install Video Transcription Pro
```powershell
cd C:\path\to\your\project
pip install -e .
```

### 5. Test Installation
```powershell
# Use full path to conda environment Python
C:\Users\%USERNAME%\anaconda3\envs\video-transcription-new\python.exe test_windows.py
```

## Method 2: Python + pip (Alternative)

### 1. Install Python
```powershell
# Download from: https://www.python.org/downloads/windows/
# Choose: Python 3.9+ (64-bit)
# ⚠️ IMPORTANT: Check "Add Python to PATH" during installation
```

### 2. Create Virtual Environment
```powershell
cd C:\path\to\your\project
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
# Install PyTorch first
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install the package
pip install -e .
```

### 4. Test
```powershell
python test_windows.py
```

---

# 🐧 Linux Installation

## Prerequisites
- Ubuntu 20.04+ / CentOS 8+ / Any modern Linux distro
- Python 3.9+
- 8GB+ RAM
- Optional: NVIDIA GPU with CUDA drivers

## Method 1: System Python (Recommended)

### 1. Install System Dependencies
```bash
# Ubuntu/Debian:
sudo apt update
sudo apt install python3-pip python3-venv ffmpeg

# CentOS/RHEL/Fedora:
sudo dnf install python3-pip python3-venv ffmpeg

# Or for older systems:
sudo yum install python3-pip ffmpeg
```

### 2. Create Virtual Environment
```bash
cd /path/to/your/project
python3 -m venv venv
source venv/bin/activate
```

### 3. Install PyTorch
```bash
# For NVIDIA GPU:
pip install torch torchvision torchaudio

# For CPU only:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 4. Install Video Transcription Pro
```bash
pip install -e .
```

### 5. Test Installation
```bash
python test_linux.py  # We'll create this
```

## Method 2: Conda on Linux

### 1. Install Miniconda
```bash
# Download and install
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
# Restart terminal or: source ~/.bashrc
```

### 2. Setup Environment
```bash
conda create -n video-transcription python=3.11
conda activate video-transcription
conda install pytorch pytorch-cuda=11.8 -c pytorch -c nvidia
```

### 3. Install Package
```bash
cd /path/to/your/project
pip install -e .
```

---

# 🐳 Docker Installation

**✅ Works on: Windows, Linux, macOS**  
**✅ No local dependencies needed**  
**✅ Guaranteed reproducible environment**

## Prerequisites
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- 8GB+ RAM
- For GPU: NVIDIA Container Toolkit

## Method 1: Pre-built Images (Coming Soon)

```bash
# CPU version (works everywhere)
docker run --rm videotranscriptionpro/video-transcription:latest-cpu --help

# GPU version (NVIDIA GPUs only)
docker run --rm --gpus all videotranscriptionpro/video-transcription:latest-gpu --help
```

## Method 2: Build from Source

### 1. Clone and Build
```bash
cd /path/to/your/project

# Build CPU image
docker build -f docker/Dockerfile.cpu -t video-transcription:cpu .

# Build GPU image (if you have NVIDIA GPU)
docker build -f docker/Dockerfile.gpu -t video-transcription:gpu .
```

### 2. Test the Container
```bash
# Test CPU version
docker run --rm video-transcription:cpu python -c "import torch; print(f'PyTorch: {torch.__version__}')"

# Test GPU version (requires nvidia-docker)
docker run --rm --gpus all video-transcription:gpu python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

### 3. Transcribe Videos
```bash
# Create folders for input/output
mkdir -p videos transcripts

# Copy your video to videos/ folder
# Then run transcription:

# CPU version
docker run --rm \
  -v "$(pwd)/videos:/app/videos:ro" \
  -v "$(pwd)/transcripts:/app/transcripts" \
  video-transcription:cpu \
  /app/videos/your_video.mp4 -o /app/transcripts

# GPU version  
docker run --rm --gpus all \
  -v "$(pwd)/videos:/app/videos:ro" \
  -v "$(pwd)/transcripts:/app/transcripts" \
  video-transcription:gpu \
  /app/videos/your_video.mp4 -o /app/transcripts --device cuda
```

---

# 🧪 Testing Your Installation

## Test Files Available

We provide platform-specific test scripts:

| Platform | Test Script | Purpose |
|----------|-------------|---------|
| Windows | `test_windows.py` | Tests Windows conda/pip installation |
| Linux | `test_linux.py` | Tests Linux installation |
| Docker | `test_docker.py` | Tests Docker container setup |

## Windows Testing

### Conda Environment Test
```powershell
# Use full path to conda environment Python
C:\Users\%USERNAME%\anaconda3\envs\video-transcription-new\python.exe test_windows.py
```

### Regular Python Test
```powershell
# If using system Python or virtual environment
python test_windows.py
```

## Linux Testing

```bash
# Activate your environment first
source venv/bin/activate  # For venv
# OR
conda activate video-transcription  # For conda

# Run test
python test_linux.py
```

## Docker Testing

```bash
# Test CPU container
docker run --rm video-transcription:cpu python test_docker.py

# Test GPU container (if available)
docker run --rm --gpus all video-transcription:gpu python test_docker.py
```

---

# 🚀 Quick Start Examples

## 1. Command Line Usage

### Windows (Conda)
```powershell
# Activate environment
conda activate video-transcription-new

# Basic transcription
video-transcribe your_video.mp4

# Advanced options
video-transcribe your_video.mp4 --model large-v3 --device cuda --speakers 2 -f txt json srt -o results/
```

### Linux
```bash
# Activate environment
source venv/bin/activate

# Basic transcription
video-transcribe your_video.mp4

# Batch processing
video-transcribe --batch /path/to/videos/ -o /path/to/output/
```

### Docker
```bash
# Create input/output folders
mkdir -p videos transcripts

# Copy your video to videos/
cp your_video.mp4 videos/

# Run transcription
docker run --rm \
  -v "$(pwd)/videos:/app/videos:ro" \
  -v "$(pwd)/transcripts:/app/transcripts" \
  video-transcription:cpu \
  /app/videos/your_video.mp4 -o /app/transcripts
```

## 2. Python API Usage

### Basic Example
```python
from video_transcription import VideoTranscriptionPipeline

# Create pipeline
pipeline = VideoTranscriptionPipeline(
    whisper_model='large-v3',  # Best quality
    device='cuda'              # Use GPU if available
)

# Transcribe video
result = pipeline.transcribe(
    input_path='your_video.mp4',
    output_dir='transcripts/',
    formats=['txt', 'json', 'srt'],
    expected_speakers=2
)

print(f"Transcription completed!")
print(f"Files created: {result.output_files}")
print(f"Processing time: {result.processing_time:.2f}s")
```

### Advanced Example with Speaker Identification
```python
from video_transcription import VideoTranscriptionPipeline

# Setup with speaker identification
pipeline = VideoTranscriptionPipeline(
    whisper_model='large-v3',
    device='cuda',
    speaker_method='pyannote',  # Best accuracy
    auth_token='your_huggingface_token'  # Required for pyannote
)

# Process with custom speaker names
speaker_mapping = {
    'Speaker 1': 'Alice',
    'Speaker 2': 'Bob'
}

result = pipeline.transcribe(
    input_path='meeting.mp4',
    output_dir='meeting_transcripts/',
    formats=['txt', 'json', 'srt'],
    expected_speakers=2,
    speaker_names=speaker_mapping
)
```

---

# 🐛 Troubleshooting

## Common Issues by Platform

### Windows Issues

#### ❌ Conda command not found
```
Error: 'conda' is not recognized
Solution: Open "Anaconda Prompt" from Start Menu instead of regular PowerShell
```

#### ❌ Python not found in conda environment
```
Error: 'python' is not recognized
Solution: Use full path:
C:\Users\%USERNAME%\anaconda3\envs\video-transcription-new\python.exe
```

#### ❌ Permission denied
```
Error: Permission denied writing to folder
Solution: Run PowerShell as Administrator or change output directory
```

### Linux Issues

#### ❌ CUDA not available
```
Error: CUDA not available but expected
Solution: 
1. Check: nvidia-smi
2. Install CUDA toolkit: sudo apt install nvidia-cuda-toolkit
3. Or use CPU: --device cpu
```

#### ❌ FFmpeg not found
```
Error: ffmpeg: command not found
Solution: sudo apt install ffmpeg
```

### Docker Issues

#### ❌ Docker daemon not running
```
Error: Cannot connect to Docker daemon
Solution: Start Docker Desktop or Docker service
```

#### ❌ GPU access in Docker
```
Error: CUDA not available in container
Solution: 
1. Install nvidia-docker2
2. Use --gpus all flag
3. Check: docker run --rm --gpus all nvidia/cuda nvidia-smi
```

#### ❌ Volume mounting issues
```
Error: Files not accessible in container
Solution: Use absolute paths for volume mounts:
-v "/full/path/to/videos:/app/videos:ro"
```

## Performance Issues

### Slow Processing
- **Use GPU**: Add `--device cuda` or `device='cuda'`
- **Smaller model**: Try `--model base` instead of `large-v3`
- **More workers**: Add `--workers 4` for batch processing

### Memory Issues
- **Reduce batch size**: Process fewer files simultaneously
- **Use smaller model**: Switch from `large-v3` to `medium` or `base`
- **Close other applications**: Free up RAM

---

# 📊 Performance Benchmarks

## Model Comparison

| Model | Size | Speed | Accuracy | Best For |
|-------|------|-------|----------|----------|
| `tiny` | 39MB | 32x faster | Good | Testing, real-time |
| `base` | 74MB | 16x faster | Better | Quick processing |
| `small` | 244MB | 6x faster | Better+ | Balanced |
| `medium` | 769MB | 2x faster | Great | High quality |
| `large-v3` | 1550MB | 1x (baseline) | Best | Production |

## Hardware Requirements

### Minimum
- **CPU**: 4 cores, 2.5GHz
- **RAM**: 8GB
- **Storage**: 5GB free space

### Recommended
- **CPU**: 8+ cores, 3.0GHz+
- **RAM**: 16GB+
- **GPU**: NVIDIA GTX 1060 or better
- **Storage**: 20GB+ SSD

### Optimal
- **CPU**: 16+ cores, 3.5GHz+
- **RAM**: 32GB+
- **GPU**: NVIDIA RTX 3070 or better
- **Storage**: 50GB+ NVMe SSD

---

# 📞 Getting Help

## Self-Help Resources
1. **Check logs**: Look for error messages in terminal output
2. **Test installation**: Run the appropriate test script
3. **Check system requirements**: Verify your hardware meets minimums
4. **Update dependencies**: Ensure PyTorch and other packages are current

## Community Support
- 📖 [Documentation](README.md)
- 🐛 [Report Issues](https://github.com/yourusername/video-transcription-pro/issues)
- 💬 [Discussions](https://github.com/yourusername/video-transcription-pro/discussions)
- 📧 [Email Support](mailto:support@example.com)

---

**🎉 Ready to start transcribing? Choose your platform above and follow the instructions!**
