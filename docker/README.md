# 🐳 Docker Configuration

This directory contains Docker configurations for Video Transcription Pro.

## 📁 Files Overview

### ✅ **Main Dockerfile** (Recommended)
- **Location**: `../Dockerfile` (in project root)
- **Type**: Multi-stage build with targets
- **Targets**: `base`, `cpu`, `gpu-base`, `gpu`, `production`
- **GPU Base Image**: `nvidia/cuda:12.1.0-runtime-ubuntu22.04` (CUDA 12.1.0)
- **Features**: 
  - Security (non-root user)
  - Health checks
  - Multi-architecture support
  - Optimized layer caching
  - Production-ready
  - Latest CUDA 12.1.0 support with Ubuntu 22.04
  - **Performance Optimized**: Slimmer base images, efficient layer structure

### ⚠️ **Individual Dockerfiles** (Deprecated)
- **`Dockerfile.cpu`** - CPU-only variant
- **`Dockerfile.gpu`** - GPU-enabled variant

**Status**: These files are deprecated and will be removed in a future version.

**Reason**: The main `Dockerfile` provides better architecture, security, and features.

## 🚀 Usage

### Using Main Dockerfile (Recommended)
```bash
# CPU variant
docker build --target cpu -t video-transcription-pro:cpu .

# GPU variant  
docker build --target gpu -t video-transcription-pro:gpu .

# Production variant (CPU with security)
docker build --target production -t video-transcription-pro:latest .
```

### Using Docker Compose (Recommended)
```bash
# CPU version
docker-compose --profile cpu up video-transcription-cpu

# GPU version
docker-compose --profile gpu up video-transcription-gpu
```

## 🔄 Migration

If you're currently using the individual Dockerfiles, migrate to the main Dockerfile:

**Before:**
```bash
docker build -f docker/Dockerfile.cpu -t my-image .
```

**After:**
```bash
docker build --target cpu -t my-image .
```

## ⚡ Performance Optimizations

### Build Performance Features:
- **🎯 Optimized Layer Caching**: Dependencies installed before source code
- **📦 Separate PyTorch Requirements**: `requirements-torch-cpu.txt` and `requirements-torch-gpu.txt`
- **🏗️ Multi-Stage Builds**: Reduced final image size
- **🧹 Aggressive Cleanup**: Minimal disk footprint
- **📋 .dockerignore**: Excludes unnecessary files from build context
- **🔧 BuildKit v0.12.0**: Latest build engine for better performance

### Expected Performance Improvements:
- **50-80% faster rebuilds** with layer caching
- **30-50% smaller images** with slimmer base images
- **20-40% faster dependency installs** with optimized requirements
- **10-30% faster builds** with reduced build context

### Monitoring Build Performance:
```bash
# Run the performance monitor script
./scripts/monitor-build-performance.sh

# Check build timing in CI/CD
time docker build --target cpu -t test-cpu .
```

## 📚 Documentation

- **[Docker Quick Start](../docs/DOCKER.md)** - Getting started guide
- **[Docker Usage Guide](../docs/docker-usage.md)** - Detailed instructions
- **[Main README](../README.md)** - Full project documentation
