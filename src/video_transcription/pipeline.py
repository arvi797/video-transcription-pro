"""
Complete video transcription pipeline with GPU acceleration.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime

from .transcriber import VideoTranscriber
from .speaker_identifier import SpeakerIdentifier
from .formatter import TranscriptFormatter


class VideoTranscriptionPipeline:
    """
    Complete video transcription pipeline with GPU acceleration.
    
    This class combines video transcription, speaker identification, and formatting
    into a streamlined pipeline for professional video processing.
    
    Attributes:
        transcriber: VideoTranscriber instance
        speaker_identifier: SpeakerIdentifier instance
        formatter: TranscriptFormatter instance
    
    Example:
        >>> pipeline = VideoTranscriptionPipeline(
        ...     whisper_model="large-v3",
        ...     device="cuda",
        ...     speaker_method="pyannote"
        ... )
        >>> result = pipeline.process_video("meeting.mp4", output_dir="transcripts/")
        >>> print(f"Processed with {result['accuracy']}% accuracy")
    """
    
    def __init__(self,
                 whisper_model: str = "large-v3",
                 device: Optional[str] = None,
                 speaker_method: Optional[str] = None,
                 auth_token: Optional[str] = None,
                 num_speakers: Optional[int] = None,
                 speaker_names: Optional[Dict] = None):
        """
        Initialize the video transcription pipeline.
        
        Args:
            whisper_model: Whisper model name ('large-v3' recommended)
            device: Computing device ('cuda', 'cpu', or None for auto-detection)
            speaker_method: Speaker identification method ('pyannote' or 'audio_clustering')
            auth_token: HuggingFace authentication token for PyAnnote
            num_speakers: Expected number of speakers
            speaker_names: Custom mapping of speaker IDs to names
        """
        self.whisper_model = whisper_model
        self.device = device
        self.speaker_method = speaker_method
        self.num_speakers = num_speakers
        self.speaker_names = speaker_names or {}
        
        # Initialize components
        self.transcriber = VideoTranscriber(model=whisper_model, device=device)
        self.speaker_identifier = SpeakerIdentifier(auth_token=auth_token)
        self.formatter = TranscriptFormatter()
        
        print(f"🚀 VideoTranscriptionPipeline initialized")
        print(f"🎯 Model: {whisper_model}")
        print(f"📱 Device: {self.transcriber.device}")
        print(f"🎭 Speaker method: {speaker_method or 'auto-detect'}")
    
    def process_video(self,
                      video_path: Union[str, Path],
                      output_dir: Optional[Union[str, Path]] = None,
                      output_formats: List[str] = None,
                      cleanup_audio: bool = True) -> Dict:
        """
        Process a video file through the complete transcription pipeline.
        
        Args:
            video_path: Path to input video file
            output_dir: Directory for output files (optional)
            output_formats: List of output formats ('txt', 'json', 'srt')
            cleanup_audio: Whether to delete extracted audio file after processing
            
        Returns:
            Dictionary containing processing results and output file paths
            
        Raises:
            FileNotFoundError: If video file doesn't exist
            Exception: If processing fails at any stage
        """
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        if output_dir is None:
            output_dir = video_path.parent / "transcripts"
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if output_formats is None:
            output_formats = ['txt', 'json']
        
        print(f"🎬 Processing video: {video_path.name}")
        print(f"📁 Output directory: {output_dir}")
        print("=" * 50)
        
        try:
            # Step 1: Extract audio
            print("🎵 Step 1: Audio extraction")
            audio_path = self.transcriber.extract_audio(str(video_path))
            
            # Step 2: Transcribe audio
            print("\n🎤 Step 2: Speech transcription")
            whisper_result = self.transcriber.transcribe(audio_path)
            
            # Step 3: Identify speakers
            print("\n🎭 Step 3: Speaker identification")
            speaker_result = self.speaker_identifier.identify_speakers(
                audio_path=audio_path,
                whisper_result=whisper_result,
                num_speakers=self.num_speakers,
                method=self.speaker_method
            )
            
            # Step 4: Generate outputs
            print("\n💾 Step 4: Generating outputs")
            output_files = {}
            
            # Generate base filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = f"{video_path.stem}_transcript_{timestamp}"
            
            # Generate requested formats
            for format_type in output_formats:
                if format_type == 'txt':
                    txt_path = output_dir / f"{base_name}.txt"
                    self.formatter.save_transcript(
                        speaker_result, 
                        txt_path, 
                        speaker_names=self.speaker_names,
                        format_style="readable"
                    )
                    output_files['txt'] = str(txt_path)
                
                elif format_type == 'json':
                    json_path = output_dir / f"{base_name}.json"
                    # Create comprehensive JSON export
                    export_data = {
                        'video_path': str(video_path),
                        'audio_path': audio_path,
                        'whisper_result': whisper_result,
                        'speaker_result': speaker_result,
                        'speaker_names': self.speaker_names,
                        'pipeline_config': {
                            'whisper_model': self.whisper_model,
                            'device': self.transcriber.device,
                            'speaker_method': speaker_result.get('method'),
                            'num_speakers': self.num_speakers
                        },
                        'processing_metadata': {
                            'timestamp': timestamp,
                            'pipeline_version': '1.0.0'
                        }
                    }
                    
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(export_data, f, indent=2, ensure_ascii=False)
                    output_files['json'] = str(json_path)
                
                elif format_type == 'srt':
                    srt_path = output_dir / f"{base_name}.srt"
                    self.formatter.save_srt(
                        speaker_result, 
                        srt_path, 
                        speaker_names=self.speaker_names
                    )
                    output_files['srt'] = str(srt_path)
            
            # Step 5: Cleanup (optional)
            if cleanup_audio:
                try:
                    Path(audio_path).unlink()
                    print(f"🗑️ Cleaned up audio file: {audio_path}")
                except Exception as e:
                    print(f"⚠️ Could not delete audio file: {e}")
            
            # Prepare result summary
            segments = speaker_result.get('segments', [])
            total_duration = segments[-1]['end'] if segments else 0
            
            result = {
                'success': True,
                'video_path': str(video_path),
                'output_files': output_files,
                'summary': {
                    'duration_minutes': total_duration / 60,
                    'num_segments': len(segments),
                    'num_speakers': speaker_result.get('num_speakers', 0),
                    'method': speaker_result.get('method', 'unknown'),
                    'accuracy': speaker_result.get('accuracy_score', 0),
                    'confidence': speaker_result.get('confidence', 'unknown'),
                    'processing_time': speaker_result.get('processing_time', 0)
                },
                'speaker_stats': self.formatter._calculate_speaker_stats(speaker_result)
            }
            
            # Print summary
            print(f"\n✅ PROCESSING COMPLETE!")
            print(f"📹 Video: {video_path.name}")
            print(f"⏱️ Duration: {total_duration/60:.1f} minutes")
            print(f"🎯 Method: {speaker_result.get('method', 'unknown').upper()}")
            print(f"📊 Accuracy: {speaker_result.get('accuracy_score', 0)}%")
            print(f"👥 Speakers: {speaker_result.get('num_speakers', 0)}")
            print(f"📝 Segments: {len(segments)}")
            print(f"📁 Files saved to: {output_dir}")
            
            return result
            
        except Exception as e:
            print(f"❌ Processing failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'video_path': str(video_path)
            }
    
    def process_audio(self,
                      audio_path: Union[str, Path],
                      output_dir: Optional[Union[str, Path]] = None,
                      output_formats: List[str] = None) -> Dict:
        """
        Process an audio file directly (skip video extraction).
        
        Args:
            audio_path: Path to input audio file
            output_dir: Directory for output files (optional)
            output_formats: List of output formats ('txt', 'json', 'srt')
            
        Returns:
            Dictionary containing processing results and output file paths
        """
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        print(f"🎵 Processing audio: {audio_path.name}")
        
        # Transcribe audio
        whisper_result = self.transcriber.transcribe(str(audio_path))
        
        # Identify speakers
        speaker_result = self.speaker_identifier.identify_speakers(
            audio_path=str(audio_path),
            whisper_result=whisper_result,
            num_speakers=self.num_speakers,
            method=self.speaker_method
        )
        
        # Use same output generation logic as process_video
        return self._generate_outputs(
            speaker_result, 
            whisper_result, 
            audio_path, 
            output_dir, 
            output_formats
        )
    
    def get_info(self) -> Dict:
        """
        Get pipeline configuration information.
        
        Returns:
            Dictionary with pipeline configuration and component status
        """
        return {
            'whisper_model': self.whisper_model,
            'device': self.transcriber.device,
            'speaker_method': self.speaker_method,
            'num_speakers': self.num_speakers,
            'speaker_names': self.speaker_names,
            'components': {
                'transcriber': self.transcriber.get_info(),
                'speaker_identifier': self.speaker_identifier.get_info()
            }
        }
