"""
High-accuracy video transcription with GPU acceleration using OpenAI Whisper.
"""

import whisper
import torch
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Union
import warnings

warnings.filterwarnings('ignore')


class VideoTranscriber:
    """
    High-accuracy video transcription with GPU acceleration.
    
    This class provides professional-grade video transcription using OpenAI Whisper
    with optimized settings for accuracy and performance.
    
    Attributes:
        device (str): Computing device ('cuda' or 'cpu')
        model_name (str): Whisper model name
        model: Loaded Whisper model instance
    
    Example:
        >>> transcriber = VideoTranscriber(model="large-v3", device="cuda")
        >>> audio_path = transcriber.extract_audio("video.mp4")
        >>> result = transcriber.transcribe(audio_path)
        >>> print(f"Transcribed {len(result['segments'])} segments")
    """
    
    def __init__(self, model: str = "large-v3", device: Optional[str] = None):
        """
        Initialize the video transcriber.
        
        Args:
            model: Whisper model name ('tiny', 'base', 'small', 'medium', 'large', 'large-v2', 'large-v3')
            device: Computing device ('cuda', 'cpu', or None for auto-detection)
        """
        # Handle device properly - ensure it's a string for Whisper
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        elif isinstance(device, torch.device):
            self.device = str(device)
        else:
            self.device = str(device)
            
        self.model_name = model
        self.model = None
        
        # Validate model name
        valid_models = ['tiny', 'base', 'small', 'medium', 'large', 'large-v2', 'large-v3']
        if model not in valid_models:
            raise ValueError(f"Invalid model '{model}'. Choose from: {valid_models}")
    
    def load_model(self) -> whisper.Whisper:
        """
        Load the Whisper model if not already loaded.
        
        Returns:
            Loaded Whisper model instance
        """
        if self.model is None:
            print(f"📥 Loading Whisper {self.model_name} on {self.device}...")
            self.model = whisper.load_model(self.model_name, device=self.device)
            print("✅ Model loaded successfully")
        return self.model
    
    def extract_audio(self, video_path: Union[str, Path], output_path: Optional[str] = None) -> str:
        """
        Extract and optimize audio from video file.
        
        Args:
            video_path: Path to input video file
            output_path: Path for output audio file (optional)
            
        Returns:
            Path to extracted audio file
            
        Raises:
            FileNotFoundError: If video file doesn't exist
            subprocess.CalledProcessError: If FFmpeg extraction fails
        """
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        if output_path is None:
            output_path = video_path.stem + "_audio_optimized.wav"
        
        output_path = Path(output_path)
        
        if output_path.exists():
            print(f"✅ Audio file already exists: {output_path}")
            return str(output_path)
        
        print(f"🎵 Extracting audio from: {video_path.name}")
        
        # FFmpeg command for optimal audio extraction
        cmd = [
            "ffmpeg", "-i", str(video_path),
            "-ar", "16000",  # 16kHz sample rate (Whisper optimized)
            "-ac", "1",      # Mono
            "-c:a", "pcm_s16le",  # 16-bit PCM
            "-y",            # Overwrite output
            str(output_path)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ Audio extracted: {output_path}")
            return str(output_path)
        except subprocess.CalledProcessError as e:
            print(f"❌ FFmpeg failed: {e}")
            print("💡 Make sure FFmpeg is installed and in PATH")
            raise
    
    def transcribe(self, audio_path: Union[str, Path], **kwargs) -> Dict:
        """
        Transcribe audio with word-level timestamps.
        
        Args:
            audio_path: Path to audio file
            **kwargs: Additional options for Whisper transcription
            
        Returns:
            Dictionary containing transcription results with segments and metadata
            
        Raises:
            FileNotFoundError: If audio file doesn't exist
        """
        self.load_model()
        
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        print(f"🎤 Transcribing: {audio_path.name}")
        print(f"⚡ Using {self.device.upper()} acceleration")
        
        # Optimal transcription settings
        options = {
            "word_timestamps": True,
            "verbose": False,
            "temperature": 0.0,  # Deterministic output
            "best_of": 5,        # Multiple passes for accuracy
            "beam_size": 2,      # Beam search for better results
            **kwargs
        }
        
        start_time = datetime.now()
        result = self.model.transcribe(str(audio_path), **options)
        end_time = datetime.now()
        
        duration = (end_time - start_time).total_seconds()
        audio_duration = result.get('segments', [])[-1]['end'] if result.get('segments') else 0
        
        print(f"✅ Transcription completed in {duration:.1f}s")
        print(f"📊 Audio: {audio_duration:.1f}s, Speed: {audio_duration/duration:.1f}x real-time")
        print(f"📝 Segments: {len(result.get('segments', []))}")
        
        # Add metadata
        result['metadata'] = {
            'model': self.model_name,
            'device': self.device,
            'processing_time': duration,
            'audio_duration': audio_duration,
            'speed_factor': audio_duration / duration if duration > 0 else 0
        }
        
        return result
    
    def get_info(self) -> Dict:
        """
        Get transcriber configuration information.
        
        Returns:
            Dictionary with transcriber configuration
        """
        return {
            'model': self.model_name,
            'device': self.device,
            'gpu_available': torch.cuda.is_available(),
            'gpu_name': torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            'model_loaded': self.model is not None
        }
