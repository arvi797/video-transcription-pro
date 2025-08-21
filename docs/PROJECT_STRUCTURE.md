# 📁 Project Structure

This document explains the organization of the Video Transcription Pro repository.

## 🏗️ Directory Structure

```
video-transcription-pro/
├── 📁 src/                          # Source code
│   └── 📁 video_transcription/      # Main package
│       ├── __init__.py
│       ├── transcriber.py           # Core transcription logic
│       ├── speaker_identifier.py    # Speaker diarization
│       ├── formatter.py             # Output formatting
│       ├── pipeline.py              # High-level pipeline
│       ├── batch_processor.py       # Batch processing
│       └── cli.py                   # Command-line interface
│
├── 📁 tests/                        # Test suite
│   ├── 📁 unit/                     # Unit tests
│   │   └── test_video_transcription.py
│   └── 📁 integration/              # Integration tests
│       ├── test_basic_functionality.py
│       ├── test_docker.py
│       ├── test_gpu_transcription.py
│       ├── test_installation.py
│       ├── test_linux.py
│       └── test_windows.py
│
├── 📁 docs/                         # Documentation
│   ├── CONTRIBUTING.md              # Contribution guidelines
│   ├── DOCKER.md                    # Docker usage guide
│   ├── INSTALL.md                   # Installation instructions
│   ├── docker-usage.md              # Docker examples
│   └── PROJECT_STRUCTURE.md         # This file
│
├── 📁 examples/                     # Usage examples
│   ├── basic_usage.py               # Basic usage example
│   ├── advanced_pipeline.py         # Advanced pipeline example
│   ├── batch_processing.py          # Batch processing example
│   └── getting_started.md           # Getting started guide
│
├── 📁 scripts/                      # Utility scripts
│   └── install_gpu.py               # GPU installation helper
│
├── 📁 docker/                       # Docker configuration
│   ├── README.md                    # Docker setup documentation
│   ├── Dockerfile.cpu               # ⚠️ Deprecated - CPU-only Docker image
│   └── Dockerfile.gpu               # ⚠️ Deprecated - GPU-enabled Docker image
│
├── 📁 .github/                      # GitHub configuration
│   └── 📁 workflows/                # CI/CD workflows
│
├── 📄 README.md                     # Main project documentation
├── 📄 LICENSE                       # MIT License
├── 📄 pyproject.toml                # Project configuration
├── 📄 setup.py                      # Package setup
├── 📄 requirements.txt              # Production dependencies
├── 📄 requirements-dev.txt          # Development dependencies
├── 📄 docker-compose.yml            # Docker Compose configuration
├── 📄 Dockerfile                    # ✅ Main multi-stage Docker image
└── 📄 .gitignore                    # Git ignore rules
```

## 🎯 Organization Principles

### 1. **Separation of Concerns**
- **Source code** in `src/` - Clean package structure
- **Tests** organized by type (unit vs integration)
- **Documentation** centralized in `docs/`
- **Examples** in dedicated `examples/` directory

### 2. **Test Organization**
- **Unit tests** (`tests/unit/`) - Test individual components
- **Integration tests** (`tests/integration/`) - Test full workflows and platform-specific functionality

### 3. **Documentation Structure**
- **User-facing docs** in root (README.md)
- **Detailed guides** in `docs/` directory
- **Examples** with clear progression from basic to advanced

### 4. **Scripts and Utilities**
- **Installation helpers** in `scripts/`
- **Docker configurations** in `docker/` (see docker/README.md for details)
- **CI/CD workflows** in `.github/workflows/`

### 5. **Docker Configuration**
- **Main Dockerfile** (root) - Multi-stage build with targets (`cpu`, `gpu`, `production`)
- **Individual Dockerfiles** (docker/) - Deprecated, use main Dockerfile instead
- **Docker Compose** - Production-ready orchestration

## 🔄 Migration Notes

This structure was reorganized from the original layout to improve:
- **Discoverability** - Easier to find relevant files
- **Maintainability** - Logical grouping of related files
- **Scalability** - Room for growth in each category
- **Best practices** - Following Python packaging standards

## 📝 File Naming Conventions

- **Python files**: snake_case (e.g., `speaker_identifier.py`)
- **Documentation**: UPPER_CASE.md (e.g., `CONTRIBUTING.md`)
- **Directories**: lowercase with hyphens (e.g., `video-transcription-pro`)
- **Test files**: `test_*.py` prefix