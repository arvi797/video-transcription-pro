# 🐳 Docker Quick Start

This directory contains everything you need to run Video Transcription Pro with Docker across any operating system.

## 🚀 One-Minute Setup

### 1. Create your workspace:
```bash
mkdir video-transcription && cd video-transcription
mkdir videos transcripts config
```

### 2. Download configuration:
```bash
# Download docker-compose.yml
curl -O https://raw.githubusercontent.com/yourusername/video-transcription-pro/main/docker-compose.yml

# Or create manually (see docker-compose.yml in this repo)
```

### 3. Add your videos:
```bash
# Copy your videos to the videos/ folder
cp /path/to/your/video.mp4 videos/
```

### 4. Run transcription:
```bash
# CPU version (works on all systems)
docker-compose --profile cpu up video-transcription-cpu

# GPU version (Linux/Windows WSL2 with NVIDIA)
docker-compose --profile gpu up video-transcription-gpu
```

Your transcripts will appear in the `transcripts/` folder!

## 📋 What You Get

- **Cross-platform compatibility**: Works on Windows, Linux, and macOS
- **No dependency hell**: Everything bundled in the container  
- **GPU acceleration**: Automatic NVIDIA GPU detection and usage
- **Multiple output formats**: TXT, JSON, and SRT subtitle files
- **Professional quality**: 95%+ speaker identification accuracy

## 🎯 Common Commands

```bash
# Single video transcription
docker run --rm \
  -v "$(pwd)/videos:/app/videos:ro" \
  -v "$(pwd)/transcripts:/app/transcripts" \
  videotranscriptionpro/video-transcription-pro:latest-cpu \
  /app/videos/your_video.mp4 -o /app/transcripts

# Batch process entire folder
docker run --rm \
  -v "$(pwd)/videos:/app/videos:ro" \
  -v "$(pwd)/transcripts:/app/transcripts" \
  videotranscriptionpro/video-transcription-pro:latest-cpu \
  --batch /app/videos -o /app/transcripts --recursive

# High-accuracy with GPU
docker run --rm --gpus all \
  -v "$(pwd)/videos:/app/videos:ro" \
  -v "$(pwd)/transcripts:/app/transcripts" \
  videotranscriptionpro/video-transcription-pro:latest-gpu \
  /app/videos/meeting.mp4 \
  --model large-v3 --device cuda --speaker-method pyannote
```

## 🔗 Links

- **[Complete Docker Guide](docs/docker-usage.md)** - Detailed platform-specific instructions
- **[Main README](README.md)** - Full project documentation
- **[Examples](examples/)** - Usage examples and tutorials

---

**Need help?** Open an [issue](https://github.com/yourusername/video-transcription-pro/issues) or check the [troubleshooting guide](docs/troubleshooting.md).
