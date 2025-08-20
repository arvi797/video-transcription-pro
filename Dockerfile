# Multi-stage Dockerfile for Video Transcription Pro
# Supports both CPU and GPU variants across multiple architectures

# Base stage with common dependencies
FROM python:3.10-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies with minimal footprint
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        git \
        curl \
        ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/archives/* \
    && rm -rf /tmp/* /var/tmp/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt requirements-dev.txt ./
COPY pyproject.toml setup.py ./

# CPU variant (default)
FROM base as cpu

RUN pip install --no-cache-dir \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

COPY . .
RUN pip install -e .[pyannote] && \
    rm -rf ~/.cache/pip/*

# GPU variant with CUDA support
FROM nvidia/cuda:12.1.0-devel-ubuntu22.04 as gpu-base

# Install Python 3.10 (default in Ubuntu 22.04) with aggressive cleanup
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-dev \
        ffmpeg \
        git \
        curl \
        ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/archives/* \
    && rm -rf /tmp/* /var/tmp/*

# Create symlinks for python
RUN ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility

WORKDIR /app

FROM gpu-base as gpu

# Copy requirements
COPY requirements.txt requirements-dev.txt ./
COPY pyproject.toml setup.py ./

# Install GPU-accelerated PyTorch
RUN pip install --no-cache-dir \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

COPY . .
RUN pip install -e .[all] && \
    rm -rf ~/.cache/pip/*

# Final production stage (CPU by default)
FROM cpu as production

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import video_transcription; print('OK')" || exit 1

# Default command
ENTRYPOINT ["python", "-m", "video_transcription.cli"]
CMD ["--help"]

# Labels for metadata
LABEL org.opencontainers.image.title="Video Transcription Pro" \
      org.opencontainers.image.description="Professional video transcription with GPU acceleration" \
      org.opencontainers.image.vendor="Video Transcription Pro" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.source="https://github.com/yourusername/video-transcription-pro" \
      org.opencontainers.image.documentation="https://video-transcription-pro.readthedocs.io/"
