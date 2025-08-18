#!/usr/bin/env python3
"""
Automated GPU installation script for video-transcription-pro.
This script automatically detects and installs the appropriate PyTorch version.
"""

import subprocess
import sys
import platform
import os


def run_command(command, check=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if check and result.returncode != 0:
            print(f"❌ Command failed: {command}")
            print(f"Error: {result.stderr}")
            return False
        return result
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False


def detect_cuda():
    """Detect CUDA version on the system."""
    try:
        # Try nvidia-smi
        result = run_command("nvidia-smi", check=False)
        if result and result.returncode == 0:
            # Parse CUDA version from nvidia-smi output
            for line in result.stdout.split("\n"):
                if "CUDA Version:" in line:
                    cuda_version = line.split("CUDA Version:")[1].strip()
                    return cuda_version
    except:
        pass

    # Try environment variables
    cuda_version = os.environ.get("CUDA_VERSION")
    if cuda_version:
        return cuda_version

    return None


def get_pytorch_url(cuda_version):
    """Get the appropriate PyTorch installation URL based on CUDA version."""
    if not cuda_version:
        return "https://download.pytorch.org/whl/cpu"

    # Map CUDA versions to PyTorch URLs
    cuda_mapping = {
        "12.1": "https://download.pytorch.org/whl/cu121",
        "12.0": "https://download.pytorch.org/whl/cu121",
        "11.8": "https://download.pytorch.org/whl/cu118",
        "11.7": "https://download.pytorch.org/whl/cu117",
        "11.6": "https://download.pytorch.org/whl/cu116",
    }

    # Extract major.minor version
    cuda_major_minor = ".".join(cuda_version.split(".")[:2])

    return cuda_mapping.get(cuda_major_minor, "https://download.pytorch.org/whl/cu118")


def install_pytorch_gpu():
    """Install PyTorch with GPU support."""
    print("🔍 Detecting CUDA version...")
    cuda_version = detect_cuda()

    if cuda_version:
        print(f"✅ CUDA {cuda_version} detected")
        pytorch_url = get_pytorch_url(cuda_version)
        print(f"📦 Installing PyTorch from: {pytorch_url}")

        # Install PyTorch with CUDA
        command = f"pip install torch torchaudio torchvision --index-url {pytorch_url}"
        if run_command(command):
            print("✅ PyTorch GPU installation successful")
            return True
        else:
            print("❌ PyTorch GPU installation failed")
            return False
    else:
        print("⚠️ CUDA not detected, installing CPU version")
        command = "pip install torch torchaudio torchvision --index-url https://download.pytorch.org/whl/cpu"
        if run_command(command):
            print("✅ PyTorch CPU installation successful")
            return False
        else:
            print("❌ PyTorch installation failed")
            return False


def verify_gpu():
    """Verify GPU support is working."""
    print("🔍 Verifying GPU support...")

    verify_script = """
import torch
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"CUDA version: {torch.version.cuda}")
    print(f"GPU device: {torch.cuda.get_device_name(0)}")
    print(f"GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
else:
    print("⚠️ CUDA not available - will use CPU")
"""

    result = run_command(f'python -c "{verify_script}"', check=False)
    if result and result.returncode == 0:
        print(result.stdout)
        return True
    else:
        print("❌ GPU verification failed")
        return False


def main():
    """Main installation function."""
    print("🚀 Video Transcription Pro - GPU Installation")
    print("=" * 50)

    # Check if we're in a virtual environment
    if not hasattr(sys, "real_prefix") and not (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        print("⚠️ Warning: Not in a virtual environment")
        print("   Consider creating one: python -m venv venv")
        response = input("   Continue anyway? (y/N): ")
        if response.lower() != "y":
            return

    # Install PyTorch with GPU support
    gpu_available = install_pytorch_gpu()

    # Install the package
    print("📦 Installing video-transcription-pro...")
    if run_command("pip install -e ."):
        print("✅ Package installation successful")
    else:
        print("❌ Package installation failed")
        return

    # Verify GPU support
    verify_gpu()

    # Test import
    print("🧪 Testing package import...")
    if run_command(
        'python -c "import video_transcription; print("✅ Package imported successfully!")"'
    ):
        print("✅ All installations completed successfully!")

        if gpu_available:
            print("\n🎉 GPU support is ready!")
            print("   You can now use device='cuda' in your code")
        else:
            print("\n⚠️ GPU support not available")
            print("   The package will use CPU (slower but functional)")
    else:
        print("❌ Package import failed")


if __name__ == "__main__":
    main()
