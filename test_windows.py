#!/usr/bin/env python3
"""
Test script to verify Video Transcription Pro installation on Windows.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_basic_imports():
    """Test basic package imports."""
    print("🧪 Testing basic imports...")
    
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__} - CUDA: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"🚀 GPU: {torch.cuda.get_device_name()}")
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False
    
    try:
        import whisper
        print("✅ OpenAI Whisper imported")
        models = whisper.available_models()
        print(f"📋 Available models: {models}")
    except ImportError as e:
        print(f"❌ Whisper import failed: {e}")
        return False
    
    try:
        import librosa
        print(f"✅ Librosa {librosa.__version__}")
    except ImportError as e:
        print(f"❌ Librosa import failed: {e}")
        return False
    
    return True

def test_video_transcription_modules():
    """Test our video transcription modules."""
    print("\n🎥 Testing Video Transcription modules...")
    
    try:
        from video_transcription import VideoTranscriber
        print("✅ VideoTranscriber imported")
    except ImportError as e:
        print(f"❌ VideoTranscriber import failed: {e}")
        return False
    
    try:
        from video_transcription import SpeakerIdentifier
        print("✅ SpeakerIdentifier imported")
    except ImportError as e:
        print(f"❌ SpeakerIdentifier import failed: {e}")
        return False
    
    try:
        from video_transcription import TranscriptFormatter
        print("✅ TranscriptFormatter imported")
    except ImportError as e:
        print(f"❌ TranscriptFormatter import failed: {e}")
        return False
    
    try:
        from video_transcription import VideoTranscriptionPipeline
        print("✅ VideoTranscriptionPipeline imported")
    except ImportError as e:
        print(f"❌ VideoTranscriptionPipeline import failed: {e}")
        return False
    
    return True

def test_whisper_model_loading():
    """Test loading a small Whisper model."""
    print("\n🤖 Testing Whisper model loading...")
    
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
    print("\n⚙️ Testing basic functionality...")
    
    try:
        from video_transcription import VideoTranscriber
        
        # Initialize with tiny model for testing
        transcriber = VideoTranscriber(model="tiny", device="cpu")
        print("✅ VideoTranscriber initialized with tiny model")
        
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🎯 Video Transcription Pro - Windows Test Suite")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Video Transcription Modules", test_video_transcription_modules),
        ("Whisper Model Loading", test_whisper_model_loading),
        ("Basic Functionality", test_basic_functionality),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your Video Transcription Pro installation is working!")
        print("\n🚀 Next steps:")
        print("1. Place a video file in this directory")
        print("2. Run a transcription test:")
        print("   python -c \"import sys; sys.path.insert(0, 'src'); from video_transcription import VideoTranscriber; t = VideoTranscriber('tiny'); print('Ready for transcription!')\"")
    else:
        print(f"\n⚠️ {total-passed} test(s) failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
