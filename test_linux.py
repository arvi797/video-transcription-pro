#!/usr/bin/env python3
"""
🐧 Video Transcription Pro - Linux Test Suite
==============================================
Comprehensive test script for Linux installations.
"""

import sys
import os
import subprocess
import importlib
from pathlib import Path


def print_header():
    """Print test suite header."""
    print("🐧 Video Transcription Pro - Linux Test Suite")
    print("=" * 50)


def test_basic_imports():
    """Test basic imports and system information."""
    print("🧪 Testing basic imports...")

    try:
        # Test PyTorch
        import torch

        cuda_available = torch.cuda.is_available()
        print(f"✅ PyTorch {torch.__version__} - CUDA: {cuda_available}")

        if cuda_available:
            gpu_name = torch.cuda.get_device_name(0)
            print(f"🚀 GPU: {gpu_name}")
        else:
            print("💻 Using CPU (CUDA not available)")

        return True
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False


def test_whisper():
    """Test OpenAI Whisper import and model availability."""
    try:
        import whisper

        print("✅ OpenAI Whisper imported")

        # List available models
        models = whisper.available_models()
        print(f"📋 Available models: {models}")
        return True
    except ImportError as e:
        print(f"❌ Whisper import failed: {e}")
        return False


def test_audio_processing():
    """Test audio processing libraries."""
    try:
        import librosa

        print(f"✅ Librosa {librosa.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Librosa import failed: {e}")
        return False


def test_video_transcription_modules():
    """Test video transcription package modules."""
    print("🎥 Testing Video Transcription modules...")

    modules_to_test = [
        "video_transcription.transcriber",
        "video_transcription.speaker_identifier",
        "video_transcription.formatter",
        "video_transcription.pipeline",
    ]

    success_count = 0
    for module_name in modules_to_test:
        try:
            # Add src to path if not already there
            src_path = Path(__file__).parent / "src"
            if str(src_path) not in sys.path:
                sys.path.insert(0, str(src_path))

            importlib.import_module(module_name)
            class_name = (
                module_name.split(".")[-1].replace("_", " ").title().replace(" ", "")
            )
            print(f"✅ {class_name} imported")
            success_count += 1
        except ImportError as e:
            print(f"❌ {module_name} import failed: {e}")

    return success_count == len(modules_to_test)


def test_whisper_model_loading():
    """Test loading a small Whisper model."""
    print("🤖 Testing Whisper model loading...")

    try:
        import whisper

        print("Loading tiny model (fastest, smallest)...")
        model = whisper.load_model("tiny")
        print("✅ Whisper tiny model loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False


def test_basic_functionality():
    """Test basic VideoTranscriber functionality."""
    print("⚙️ Testing basic functionality...")

    try:
        # Add src to path
        src_path = Path(__file__).parent / "src"
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        from video_transcription.transcriber import VideoTranscriber

        # Initialize with tiny model for speed
        transcriber = VideoTranscriber(model_name="tiny", device="cpu")
        print("✅ VideoTranscriber initialized with tiny model")
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False


def test_system_dependencies():
    """Test system-level dependencies."""
    print("🔧 Testing system dependencies...")

    # Test FFmpeg
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            # Extract version from first line
            version_line = result.stdout.split("\n")[0]
            print(f"✅ {version_line}")
            return True
        else:
            print("❌ FFmpeg not working properly")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg not found - install with: sudo apt install ffmpeg")
        return False
    except subprocess.TimeoutExpired:
        print("❌ FFmpeg command timed out")
        return False


def check_cuda_environment():
    """Check CUDA environment setup."""
    print("🔍 Checking CUDA environment...")

    try:
        # Check nvidia-smi
        result = subprocess.run(
            ["nvidia-smi"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            print("✅ NVIDIA drivers installed")
            # Extract GPU info
            lines = result.stdout.split("\n")
            for line in lines:
                if "GeForce" in line or "RTX" in line or "GTX" in line:
                    gpu_info = line.strip().split("|")[1].strip()
                    print(f"🎮 GPU: {gpu_info}")
                    break
            return True
        else:
            print("⚠️ nvidia-smi failed - GPU acceleration may not work")
            return False
    except FileNotFoundError:
        print("⚠️ nvidia-smi not found - install NVIDIA drivers for GPU support")
        return False
    except subprocess.TimeoutExpired:
        print("❌ nvidia-smi command timed out")
        return False


def run_all_tests():
    """Run all tests and report results."""
    print_header()

    tests = [
        ("Basic Imports", test_basic_imports),
        ("Audio Processing", test_audio_processing),
        ("Whisper", test_whisper),
        ("Video Transcription Modules", test_video_transcription_modules),
        ("Whisper Model Loading", test_whisper_model_loading),
        ("Basic Functionality", test_basic_functionality),
        ("System Dependencies", test_system_dependencies),
        ("CUDA Environment", check_cuda_environment),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
        print()  # Add spacing between tests

    # Print results summary
    print("=" * 50)
    print("📊 Test Results:")
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1

    total = len(results)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print(
            "🎉 All tests passed! Your Video Transcription Pro installation is working!"
        )
        print("🚀 Next steps:")
        print("1. Place a video file in this directory")
        print("2. Run a transcription test:")
        print(
            "   python -c \"from video_transcription import VideoTranscriber; t = VideoTranscriber('tiny'); print('Ready for transcription!')\""
        )
    else:
        print(f"⚠️ {total - passed} test(s) failed. Please check the errors above.")

        # Provide specific help based on failures
        failed_tests = [name for name, result in results if not result]

        if "Basic Imports" in failed_tests:
            print("\n🔧 To fix import issues:")
            print("   pip install torch torchvision torchaudio")
            print("   pip install openai-whisper librosa")

        if "System Dependencies" in failed_tests:
            print("\n🔧 To install FFmpeg:")
            print("   sudo apt install ffmpeg  # Ubuntu/Debian")
            print("   sudo dnf install ffmpeg  # Fedora/CentOS")

        if "CUDA Environment" in failed_tests:
            print("\n🔧 For GPU support:")
            print("   1. Install NVIDIA drivers")
            print("   2. Install CUDA toolkit: sudo apt install nvidia-cuda-toolkit")
            print("   3. Or use CPU mode: --device cpu")


if __name__ == "__main__":
    run_all_tests()
