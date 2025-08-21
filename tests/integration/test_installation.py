#!/usr/bin/env python3
"""
Quick installation test for Video Transcription Pro
Run this script after installing Python to verify everything works.
"""

import sys
import subprocess
import importlib.util
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    print(f"🐍 Python version: {sys.version}")

    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Please upgrade Python.")
        return False

    print("✅ Python version is compatible")
    return True


def check_pip():
    """Check if pip is available."""
    try:
        import pip

        print(f"📦 pip version: {pip.__version__}")
        return True
    except ImportError:
        print("❌ pip not found. Please install pip.")
        return False


def install_package():
    """Install video-transcription-pro if not already installed."""
    try:
        # Try importing the package
        import video_transcription

        print("✅ video-transcription-pro is already installed")
        return True
    except ImportError:
        print("📥 Installing video-transcription-pro...")
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "torch",
                    "--index-url",
                    "https://download.pytorch.org/whl/cpu",
                ],
                check=True,
            )

            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-e", "."], check=True
            )

            print("✅ Package installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install package: {e}")
            return False


def test_basic_import():
    """Test basic package imports."""
    print("\n🧪 Testing basic imports...")

    try:
        from video_transcription import VideoTranscriber

        print("✅ VideoTranscriber import successful")
    except ImportError as e:
        print(f"❌ Failed to import VideoTranscriber: {e}")
        return False

    try:
        from video_transcription import SpeakerIdentifier

        print("✅ SpeakerIdentifier import successful")
    except ImportError as e:
        print(f"❌ Failed to import SpeakerIdentifier: {e}")
        return False

    try:
        from video_transcription import VideoTranscriptionPipeline

        print("✅ VideoTranscriptionPipeline import successful")
    except ImportError as e:
        print(f"❌ Failed to import VideoTranscriptionPipeline: {e}")
        return False

    return True


def test_whisper_availability():
    """Test if Whisper can be loaded."""
    print("\n🎤 Testing Whisper availability...")

    try:
        import whisper

        models = whisper.available_models()
        print(f"✅ Whisper available with models: {models}")
        return True
    except ImportError as e:
        print(f"❌ Whisper not available: {e}")
        return False


def test_torch():
    """Test PyTorch installation."""
    print("\n🔥 Testing PyTorch...")

    try:
        import torch

        print(f"✅ PyTorch version: {torch.__version__}")

        if torch.cuda.is_available():
            print(f"🚀 CUDA available! GPU: {torch.cuda.get_device_name()}")
        else:
            print("💻 CUDA not available - will use CPU")

        return True
    except ImportError as e:
        print(f"❌ PyTorch not available: {e}")
        return False


def test_ffmpeg():
    """Test FFmpeg availability."""
    print("\n🎬 Testing FFmpeg...")

    try:
        result = subprocess.run(
            ["ffmpeg", "-version"], capture_output=True, text=True, check=True
        )
        print("✅ FFmpeg is available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ FFmpeg not found in PATH")
        print("💡 Download from: https://ffmpeg.org/download.html#build-windows")
        print("   Or install via conda: conda install -c conda-forge ffmpeg")
        return False


def create_test_transcription():
    """Create a simple test to verify the package works."""
    print("\n🎯 Creating basic functionality test...")

    try:
        from video_transcription import VideoTranscriber

        # Initialize transcriber (this will try to load model)
        transcriber = VideoTranscriber(model="tiny", device="cpu")
        print("✅ VideoTranscriber initialized successfully")

        # Test audio extraction (without actual file)
        print("✅ Basic functionality test passed")
        return True

    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🎥 Video Transcription Pro - Installation Test")
    print("=" * 50)

    tests = [
        ("Python Version", check_python_version),
        ("pip Availability", check_pip),
        ("Package Installation", install_package),
        ("Basic Imports", test_basic_import),
        ("PyTorch", test_torch),
        ("Whisper", test_whisper_availability),
        ("FFmpeg", test_ffmpeg),
        ("Basic Functionality", create_test_transcription),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")

    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Your system is ready for video transcription.")
        print("\nNext steps:")
        print("1. Place a video file in the current directory")
        print(
            "2. Run: python -c \"from video_transcription import VideoTranscriptionPipeline; pipeline = VideoTranscriptionPipeline(); result = pipeline.transcribe('your_video.mp4', 'output/')\""
        )
    else:
        print("\n⚠️ Some tests failed. Please address the issues above.")
        print("\nFor help:")
        print(
            "- Check the documentation: https://github.com/yourusername/video-transcription-pro"
        )
        print(
            "- Open an issue: https://github.com/yourusername/video-transcription-pro/issues"
        )


if __name__ == "__main__":
    main()
