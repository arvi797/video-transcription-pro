#!/usr/bin/env python3
"""
🐳 Video Transcription Pro - Docker Test Suite
===============================================
Test script specifically designed for Docker containers.
"""

import sys
import os
import subprocess
import importlib
from pathlib import Path

def print_header():
    """Print test suite header."""
    print("🐳 Video Transcription Pro - Docker Test Suite")
    print("=" * 50)

def test_container_environment():
    """Test Docker container environment."""
    print("📦 Testing container environment...")
    
    # Check if running in container
    if os.path.exists('/.dockerenv'):
        print("✅ Running inside Docker container")
    else:
        print("⚠️ Not running in Docker container")
    
    # Check Python version
    print(f"🐍 Python version: {sys.version}")
    
    # Check architecture
    import platform
    print(f"🏗️ Architecture: {platform.machine()}")
    print(f"💻 Platform: {platform.platform()}")
    
    return True

def test_pytorch_installation():
    """Test PyTorch installation and CUDA availability."""
    print("🔥 Testing PyTorch installation...")
    
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__}")
        
        # Check CUDA
        cuda_available = torch.cuda.is_available()
        print(f"🚀 CUDA available: {cuda_available}")
        
        if cuda_available:
            device_count = torch.cuda.device_count()
            print(f"🎮 CUDA devices: {device_count}")
            
            for i in range(device_count):
                device_name = torch.cuda.get_device_name(i)
                print(f"   Device {i}: {device_name}")
        else:
            print("💻 Using CPU mode")
        
        # Test tensor operations
        x = torch.randn(3, 3)
        if cuda_available:
            x_gpu = x.cuda()
            print("✅ GPU tensor operations working")
        
        print("✅ CPU tensor operations working")
        return True
        
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ PyTorch test failed: {e}")
        return False

def test_whisper_installation():
    """Test OpenAI Whisper installation."""
    print("🎤 Testing Whisper installation...")
    
    try:
        import whisper
        print("✅ OpenAI Whisper imported")
        
        # List models
        models = whisper.available_models()
        print(f"📋 Available models: {models}")
        
        # Test model loading
        print("Loading tiny model...")
        model = whisper.load_model("tiny")
        print("✅ Tiny model loaded successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Whisper import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Whisper test failed: {e}")
        return False

def test_audio_libraries():
    """Test audio processing libraries."""
    print("🎵 Testing audio libraries...")
    
    success = True
    
    # Test librosa
    try:
        import librosa
        print(f"✅ Librosa {librosa.__version__}")
    except ImportError as e:
        print(f"❌ Librosa import failed: {e}")
        success = False
    
    # Test soundfile
    try:
        import soundfile
        print(f"✅ SoundFile imported")
    except ImportError as e:
        print(f"❌ SoundFile import failed: {e}")
        success = False
    
    # Test scipy
    try:
        import scipy
        print(f"✅ SciPy {scipy.__version__}")
    except ImportError as e:
        print(f"❌ SciPy import failed: {e}")
        success = False
    
    # Test numpy
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__}")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        success = False
    
    return success

def test_video_processing():
    """Test video processing capabilities."""
    print("🎬 Testing video processing...")
    
    try:
        # Test ffmpeg-python
        import ffmpeg
        print("✅ ffmpeg-python imported")
        
        # Test FFmpeg binary
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            # Extract version from first line
            version_line = result.stdout.split('\n')[0]
            print(f"✅ {version_line}")
            return True
        else:
            print("❌ FFmpeg binary not working")
            return False
            
    except ImportError as e:
        print(f"❌ ffmpeg-python import failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ FFmpeg binary not found")
        return False
    except subprocess.TimeoutExpired:
        print("❌ FFmpeg command timed out")
        return False
    except Exception as e:
        print(f"❌ Video processing test failed: {e}")
        return False

def test_package_modules():
    """Test video transcription package modules."""
    print("📦 Testing package modules...")
    
    # Check if package is installed
    try:
        import video_transcription
        print("✅ video_transcription package imported")
        
        # Test main classes
        from video_transcription import VideoTranscriber
        print("✅ VideoTranscriber imported")
        
        from video_transcription import VideoTranscriptionPipeline
        print("✅ VideoTranscriptionPipeline imported")
        
        # Test initialization
        transcriber = VideoTranscriber(model_name='tiny', device='cpu')
        print("✅ VideoTranscriber initialized")
        
        return True
        
    except ImportError as e:
        print(f"❌ Package import failed: {e}")
        print("💡 Make sure the package is properly installed in the container")
        return False
    except Exception as e:
        print(f"❌ Package test failed: {e}")
        return False

def test_file_system():
    """Test file system access and permissions."""
    print("📁 Testing file system...")
    
    try:
        # Test current directory
        cwd = os.getcwd()
        print(f"📍 Current directory: {cwd}")
        
        # Test write permissions
        test_file = Path("test_write_permissions.txt")
        test_file.write_text("test")
        test_file.unlink()
        print("✅ Write permissions OK")
        
        # Check for expected directories
        expected_dirs = ['/app', '/tmp']
        for dir_path in expected_dirs:
            if os.path.exists(dir_path):
                print(f"✅ Directory exists: {dir_path}")
            else:
                print(f"⚠️ Directory missing: {dir_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ File system test failed: {e}")
        return False

def test_memory_and_resources():
    """Test available memory and resources."""
    print("💾 Testing memory and resources...")
    
    try:
        import psutil
        
        # Memory info
        memory = psutil.virtual_memory()
        print(f"💾 Total memory: {memory.total // (1024**3):.1f} GB")
        print(f"💾 Available memory: {memory.available // (1024**3):.1f} GB")
        
        # CPU info
        cpu_count = psutil.cpu_count()
        print(f"🔧 CPU cores: {cpu_count}")
        
        # Disk space
        disk = psutil.disk_usage('/')
        print(f"💿 Disk space: {disk.free // (1024**3):.1f} GB free")
        
        return True
        
    except ImportError:
        print("⚠️ psutil not available - skipping detailed resource check")
        return True
    except Exception as e:
        print(f"❌ Resource check failed: {e}")
        return False

def run_docker_tests():
    """Run all Docker-specific tests."""
    print_header()
    
    tests = [
        ("Container Environment", test_container_environment),
        ("PyTorch Installation", test_pytorch_installation),
        ("Whisper Installation", test_whisper_installation),
        ("Audio Libraries", test_audio_libraries),
        ("Video Processing", test_video_processing),
        ("Package Modules", test_package_modules),
        ("File System", test_file_system),
        ("Memory and Resources", test_memory_and_resources),
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
    print("📊 Docker Test Results:")
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Docker tests passed! Container is ready for transcription!")
        print("🚀 Next steps:")
        print("1. Mount your video files: -v /host/videos:/app/videos")
        print("2. Mount output directory: -v /host/output:/app/output") 
        print("3. Run transcription: video-transcribe /app/videos/your_video.mp4")
    else:
        print(f"⚠️ {total - passed} test(s) failed.")
        
        # Provide Docker-specific troubleshooting
        failed_tests = [name for name, result in results if not result]
        
        if "PyTorch Installation" in failed_tests:
            print("\n🔧 PyTorch issues:")
            print("   - Rebuild container with correct PyTorch version")
            print("   - For GPU: ensure nvidia-docker is installed on host")
        
        if "Package Modules" in failed_tests:
            print("\n🔧 Package issues:")
            print("   - Ensure package is installed in Dockerfile")
            print("   - Check PYTHONPATH in container")
        
        if "Video Processing" in failed_tests:
            print("\n🔧 FFmpeg issues:")
            print("   - Install FFmpeg in Dockerfile")
            print("   - Check PATH in container")

if __name__ == "__main__":
    run_docker_tests()
