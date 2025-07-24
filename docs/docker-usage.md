# 🐳 Docker Usage Guide

This guide shows you how to use Video Transcription Pro with Docker across different operating systems and hardware configurations.

## 🚀 Quick Start

### Pull the Image

```bash
# CPU version (works on all systems)
docker pull videotranscriptionpro/video-transcription-pro:latest-cpu

# GPU version (requires NVIDIA GPU + Docker GPU support)
docker pull videotranscriptionpro/video-transcription-pro:latest-gpu
```

### Basic Usage

```bash
# Transcribe a single video (CPU)
docker run --rm -v "$(pwd)/videos:/app/videos" -v "$(pwd)/transcripts:/app/transcripts" \
  videotranscriptionpro/video-transcription-pro:latest-cpu \
  /app/videos/your_video.mp4 -o /app/transcripts

# Transcribe with GPU acceleration
docker run --rm --gpus all \
  -v "$(pwd)/videos:/app/videos" -v "$(pwd)/transcripts:/app/transcripts" \
  videotranscriptionpro/video-transcription-pro:latest-gpu \
  /app/videos/your_video.mp4 -o /app/transcripts --device cuda
```

## 🖥️ Platform-Specific Instructions

### Windows (PowerShell)

```powershell
# CPU version
docker run --rm -v "${PWD}/videos:/app/videos" -v "${PWD}/transcripts:/app/transcripts" `
  videotranscriptionpro/video-transcription-pro:latest-cpu `
  /app/videos/your_video.mp4 -o /app/transcripts

# GPU version (requires WSL2 + NVIDIA Container Toolkit)
docker run --rm --gpus all `
  -v "${PWD}/videos:/app/videos" -v "${PWD}/transcripts:/app/transcripts" `
  videotranscriptionpro/video-transcription-pro:latest-gpu `
  /app/videos/your_video.mp4 -o /app/transcripts --device cuda
```

### Windows (Command Prompt)

```cmd
REM CPU version
docker run --rm -v "%cd%/videos:/app/videos" -v "%cd%/transcripts:/app/transcripts" ^
  videotranscriptionpro/video-transcription-pro:latest-cpu ^
  /app/videos/your_video.mp4 -o /app/transcripts

REM GPU version
docker run --rm --gpus all ^
  -v "%cd%/videos:/app/videos" -v "%cd%/transcripts:/app/transcripts" ^
  videotranscriptionpro/video-transcription-pro:latest-gpu ^
  /app/videos/your_video.mp4 -o /app/transcripts --device cuda
```

### Linux/macOS

```bash
# CPU version
docker run --rm -v "$(pwd)/videos:/app/videos" -v "$(pwd)/transcripts:/app/transcripts" \
  videotranscriptionpro/video-transcription-pro:latest-cpu \
  /app/videos/your_video.mp4 -o /app/transcripts

# GPU version (Linux only)
docker run --rm --gpus all \
  -v "$(pwd)/videos:/app/videos" -v "$(pwd)/transcripts:/app/transcripts" \
  videotranscriptionpro/video-transcription-pro:latest-gpu \
  /app/videos/your_video.mp4 -o /app/transcripts --device cuda
```

## 🔧 Docker Compose (Recommended)

### Setup

1. **Create project structure:**
```
video-transcription/
├── videos/          # Input videos
├── transcripts/     # Output transcripts  
├── config/         # Configuration files
└── docker-compose.yml
```

2. **Download docker-compose.yml:**
```bash
curl -O https://raw.githubusercontent.com/yourusername/video-transcription-pro/main/docker-compose.yml
```

### Usage Examples

```bash
# CPU processing
docker-compose --profile cpu up video-transcription-cpu

# GPU processing (Linux only)
docker-compose --profile gpu up video-transcription-gpu

# Batch processing
docker-compose --profile batch up batch-processor

# Interactive shell
docker-compose run video-transcription-cpu bash
```

## 🎯 Common Use Cases

### 1. Single Video Transcription

```bash
# Place video in ./videos/ folder
# Run transcription
docker run --rm \
  -v "$(pwd)/videos:/app/videos:ro" \
  -v "$(pwd)/transcripts:/app/transcripts" \
  videotranscriptionpro/video-transcription-pro:latest-cpu \
  /app/videos/meeting.mp4 -o /app/transcripts -f txt json srt
```

### 2. Batch Processing

```bash
# Process entire folder
docker run --rm \
  -v "$(pwd)/videos:/app/videos:ro" \
  -v "$(pwd)/batch_output:/app/transcripts" \
  videotranscriptionpro/video-transcription-pro:latest-cpu \
  --batch /app/videos -o /app/transcripts --workers 2 --recursive
```

### 3. High-Accuracy Processing

```bash
# Use best model with speaker identification
docker run --rm --gpus all \
  -v "$(pwd)/videos:/app/videos:ro" \
  -v "$(pwd)/transcripts:/app/transcripts" \
  videotranscriptionpro/video-transcription-pro:latest-gpu \
  /app/videos/interview.mp4 \
  --model large-v3 \
  --device cuda \
  --speaker-method pyannote \
  --speakers 2 \
  -f txt json srt
```

### 4. Custom Configuration

```bash
# Create config file
echo '{"Speaker_A": "John Doe", "Speaker_B": "Jane Smith"}' > config/speakers.json

# Use custom speaker names
docker run --rm \
  -v "$(pwd)/videos:/app/videos:ro" \
  -v "$(pwd)/transcripts:/app/transcripts" \
  -v "$(pwd)/config:/app/config:ro" \
  videotranscriptionpro/video-transcription-pro:latest-cpu \
  /app/videos/conversation.mp4 \
  --speaker-names /app/config/speakers.json \
  -o /app/transcripts
```

## ⚙️ GPU Setup Requirements

### Windows (WSL2)

1. **Install WSL2 and Docker Desktop**
2. **Install NVIDIA Container Toolkit:**
```bash
# In WSL2 terminal
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

3. **Test GPU access:**
```bash
docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu20.04 nvidia-smi
```

### Linux

1. **Install NVIDIA Container Toolkit:**
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

2. **Test:**
```bash
docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu20.04 nvidia-smi
```

### macOS

GPU acceleration is not available on macOS. Use CPU version:
```bash
docker run --rm \
  -v "$(pwd)/videos:/app/videos:ro" \
  -v "$(pwd)/transcripts:/app/transcripts" \
  videotranscriptionpro/video-transcription-pro:latest-cpu \
  /app/videos/your_video.mp4 -o /app/transcripts
```

## 🔍 Troubleshooting

### Common Issues

1. **Permission denied errors:**
```bash
# Fix file permissions (Linux/macOS)
sudo chown -R $(id -u):$(id -g) transcripts/

# Windows: Run Docker Desktop as Administrator
```

2. **GPU not detected:**
```bash
# Check GPU support
docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu20.04 nvidia-smi

# If fails, reinstall NVIDIA Container Toolkit
```

3. **Out of memory errors:**
```bash
# Use smaller model
docker run ... --model medium

# Or increase Docker memory limit in Docker Desktop settings
```

4. **FFmpeg not found:**
```bash
# This shouldn't happen with our Docker images, but if it does:
docker run --rm videotranscriptionpro/video-transcription-pro:latest-cpu which ffmpeg
```

### Performance Optimization

```bash
# Increase shared memory for large files
docker run --rm --shm-size=4g \
  -v "$(pwd)/videos:/app/videos:ro" \
  -v "$(pwd)/transcripts:/app/transcripts" \
  videotranscriptionpro/video-transcription-pro:latest-gpu \
  /app/videos/large_video.mp4 -o /app/transcripts

# Limit memory usage
docker run --rm --memory=8g \
  videotranscriptionpro/video-transcription-pro:latest-cpu \
  /app/videos/video.mp4 -o /app/transcripts
```

## 🏗️ Building Custom Images

```bash
# Build CPU version
docker build --target cpu -t my-video-transcription:cpu .

# Build GPU version  
docker build --target gpu -t my-video-transcription:gpu .

# Build with custom base image
docker build --build-arg BASE_IMAGE=python:3.10-slim -t my-video-transcription:custom .
```

## 📋 Available Images

| Image | Platform | GPU Support | Size | Use Case |
|-------|----------|-------------|------|----------|
| `latest-cpu` | linux/amd64, linux/arm64 | ❌ | ~2GB | General use, all platforms |
| `latest-gpu` | linux/amd64 | ✅ | ~4GB | High performance, NVIDIA GPUs |
| `latest` | linux/amd64, linux/arm64 | ❌ | ~2GB | Alias for latest-cpu |

## 🌐 Multi-Architecture Support

Our images support multiple architectures:

- **linux/amd64**: Intel/AMD x64 processors (most common)
- **linux/arm64**: ARM processors (Apple Silicon, Raspberry Pi 4+)

Docker automatically pulls the correct architecture for your system.

---

**Need help?** Check our [troubleshooting guide](docs/troubleshooting.md) or [open an issue](https://github.com/yourusername/video-transcription-pro/issues).
