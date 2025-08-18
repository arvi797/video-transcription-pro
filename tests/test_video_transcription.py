"""
Test suite for video-transcription-pro package.
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch

# Import the classes to test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from video_transcription import (
    VideoTranscriber, 
    SpeakerIdentifier, 
    TranscriptFormatter,
    VideoTranscriptionPipeline,
    BatchProcessor
)


class TestVideoTranscriber:
    """Test cases for VideoTranscriber class."""
    
    def test_init_default(self):
        """Test default initialization."""
        transcriber = VideoTranscriber()
        assert transcriber.model_name == "large-v3"
        assert transcriber.device in ["cuda", "cpu"]
        assert transcriber.model is None
    
    def test_init_custom(self):
        """Test custom initialization."""
        transcriber = VideoTranscriber(model="medium", device="cpu")
        assert transcriber.model_name == "medium"
        assert transcriber.device == "cpu"
    
    def test_invalid_model(self):
        """Test invalid model name raises error."""
        with pytest.raises(ValueError):
            VideoTranscriber(model="invalid_model")
    
    def test_get_info(self):
        """Test get_info method."""
        transcriber = VideoTranscriber()
        info = transcriber.get_info()
        
        assert "model" in info
        assert "device" in info
        assert "gpu_available" in info
        assert "model_loaded" in info
        
        assert info["model"] == transcriber.model_name
        assert info["device"] == transcriber.device
        assert info["model_loaded"] is False


class TestSpeakerIdentifier:
    """Test cases for SpeakerIdentifier class."""
    
    def test_init(self):
        """Test initialization."""
        identifier = SpeakerIdentifier()
        assert "pyannote" in identifier.methods_available
        assert "audio_clustering" in identifier.methods_available
        assert identifier.methods_available["audio_clustering"] is True
    
    def test_get_info(self):
        """Test get_info method."""
        identifier = SpeakerIdentifier()
        info = identifier.get_info()
        
        assert "methods_available" in info
        assert "pyannote_available" in info
        assert "gpu_available" in info
    
    @patch('video_transcription.speaker_identifier.torch')
    def test_audio_clustering_fallback(self, mock_torch):
        """Test audio clustering method."""
        mock_torch.cuda.is_available.return_value = False
        
        identifier = SpeakerIdentifier()
        
        # Mock whisper result
        whisper_result = {
            "segments": [
                {"start": 0.0, "end": 2.0, "text": "Hello there"},
                {"start": 3.0, "end": 5.0, "text": "How are you?"},
                {"start": 6.0, "end": 8.0, "text": "I'm doing well"}
            ]
        }
        
        result = identifier._audio_clustering("dummy_path", whisper_result, 2)
        
        assert result["method"] == "audio_clustering"
        assert result["accuracy_score"] == 70
        assert len(result["segments"]) == 3
        assert all("speaker" in seg for seg in result["segments"])


class TestTranscriptFormatter:
    """Test cases for TranscriptFormatter class."""
    
    def test_init(self):
        """Test initialization."""
        formatter = TranscriptFormatter()
        assert formatter is not None
    
    def test_format_timestamp(self):
        """Test timestamp formatting."""
        formatter = TranscriptFormatter()
        
        # Test single timestamp
        ts_single = formatter._format_timestamp(65.5)
        assert ts_single == "[01:05.50]"
        
        # Test timestamp range
        ts_range = formatter._format_timestamp(65.5, 70.2)
        assert ts_range == "[01:05.50-01:10.20]"
    
    def test_format_readable(self):
        """Test readable transcript formatting."""
        formatter = TranscriptFormatter()
        
        # Mock speaker result
        result = {
            "segments": [
                {"start": 0.0, "end": 2.0, "text": "Hello there", "speaker": "Speaker_A"},
                {"start": 3.0, "end": 5.0, "text": "How are you?", "speaker": "Speaker_B"},
                {"start": 6.0, "end": 8.0, "text": "I'm fine", "speaker": "Speaker_A"}
            ]
        }
        
        transcript = formatter.format_transcript(result, include_timestamps=False)
        
        assert "**Speaker_A**:" in transcript
        assert "**Speaker_B**:" in transcript
        assert "Hello there" in transcript
        assert "How are you?" in transcript
        assert "I'm fine" in transcript
    
    def test_speaker_names_replacement(self):
        """Test custom speaker names."""
        formatter = TranscriptFormatter()
        
        result = {
            "segments": [
                {"start": 0.0, "end": 2.0, "text": "Hello", "speaker": "Speaker_A"}
            ]
        }
        
        speaker_names = {"Speaker_A": "John Doe"}
        transcript = formatter.format_transcript(result, speaker_names=speaker_names)
        
        assert "**John Doe**" in transcript
        assert "**Speaker_A**" not in transcript
    
    def test_calculate_speaker_stats(self):
        """Test speaker statistics calculation."""
        formatter = TranscriptFormatter()
        
        result = {
            "segments": [
                {"start": 0.0, "end": 2.0, "text": "Hello there", "speaker": "Speaker_A"},
                {"start": 3.0, "end": 5.0, "text": "How are you doing?", "speaker": "Speaker_B"},
                {"start": 6.0, "end": 8.0, "text": "Fine", "speaker": "Speaker_A"}
            ]
        }
        
        stats = formatter._calculate_speaker_stats(result)
        
        assert "Speaker_A" in stats
        assert "Speaker_B" in stats
        
        # Speaker_A has 2 segments totaling 4 seconds
        assert stats["Speaker_A"]["segment_count"] == 2
        assert stats["Speaker_A"]["total_duration"] == 4.0
        
        # Speaker_B has 1 segment of 2 seconds  
        assert stats["Speaker_B"]["segment_count"] == 1
        assert stats["Speaker_B"]["total_duration"] == 2.0
    
    def test_seconds_to_srt_time(self):
        """Test SRT time format conversion."""
        formatter = TranscriptFormatter()
        
        # Test various timestamps
        assert formatter._seconds_to_srt_time(65.5) == "00:01:05,500"
        assert formatter._seconds_to_srt_time(3661.123) == "01:01:01,123"
        assert formatter._seconds_to_srt_time(0.0) == "00:00:00,000"


class TestVideoTranscriptionPipeline:
    """Test cases for VideoTranscriptionPipeline class."""
    
    def test_init(self):
        """Test pipeline initialization."""
        pipeline = VideoTranscriptionPipeline(
            whisper_model="medium",
            device="cpu",
            num_speakers=2
        )
        
        assert pipeline.whisper_model == "medium"
        assert pipeline.num_speakers == 2
        assert pipeline.transcriber is not None
        assert pipeline.speaker_identifier is not None
        assert pipeline.formatter is not None
    
    def test_get_info(self):
        """Test pipeline info."""
        pipeline = VideoTranscriptionPipeline()
        info = pipeline.get_info()
        
        assert "whisper_model" in info
        assert "device" in info
        assert "components" in info
        assert "transcriber" in info["components"]
        assert "speaker_identifier" in info["components"]

    def test_process_audio_generates_outputs(self, tmp_path, monkeypatch):
        """Test that processing an audio file generates transcript outputs."""
        pipeline = VideoTranscriptionPipeline()

        # Create dummy audio file
        audio_file = tmp_path / "sample.wav"
        audio_file.touch()

        # Mock transcription and speaker identification
        fake_whisper = {"segments": [{"start": 0.0, "end": 1.0, "text": "hi"}]}
        fake_speaker = {
            "segments": [{"start": 0.0, "end": 1.0, "text": "hi", "speaker": "A"}],
            "num_speakers": 1,
            "method": "audio_clustering",
            "accuracy_score": 70,
            "processing_time": 0.1,
            "confidence": "medium",
        }

        monkeypatch.setattr(pipeline.transcriber, "transcribe", lambda path: fake_whisper)

        def fake_identify(audio_path, whisper_result, num_speakers=None, method=None):
            return fake_speaker

        monkeypatch.setattr(
            pipeline.speaker_identifier, "identify_speakers", fake_identify
        )

        result = pipeline.process_audio(str(audio_file), output_dir=tmp_path)

        assert result["success"] is True
        assert Path(result["output_files"]["txt"]).exists()
        assert Path(result["output_files"]["json"]).exists()


class TestBatchProcessor:
    """Test cases for BatchProcessor class."""
    
    def test_init(self):
        """Test batch processor initialization."""
        processor = BatchProcessor(
            whisper_model="medium",
            max_workers=2,
            output_formats=["txt", "json"]
        )
        
        assert processor.max_workers == 2
        assert processor.output_formats == ["txt", "json"]
        assert len(processor.supported_extensions) > 0
    
    def test_find_media_files(self):
        """Test media file discovery."""
        processor = BatchProcessor()
        
        # Create temporary directory with test files
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test files
            (temp_path / "video1.mp4").touch()
            (temp_path / "video2.mkv").touch()
            (temp_path / "audio1.mp3").touch()
            (temp_path / "document.txt").touch()  # Should be ignored
            
            media_files = processor._find_media_files(temp_path)
            
            assert len(media_files) == 3  # Only media files
            extensions = {f.suffix for f in media_files}
            assert ".mp4" in extensions
            assert ".mkv" in extensions
            assert ".mp3" in extensions
            assert ".txt" not in extensions
    
    def test_get_info(self):
        """Test batch processor info."""
        processor = BatchProcessor()
        info = processor.get_info()
        
        assert "max_workers" in info
        assert "output_formats" in info
        assert "supported_extensions" in info
        assert "pipeline" in info


# Integration tests
class TestIntegration:
    """Integration tests for the complete package."""
    
    @pytest.fixture
    def temp_files(self):
        """Create temporary files for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create mock files
            video_file = temp_path / "test_video.mp4"
            audio_file = temp_path / "test_audio.wav"
            output_dir = temp_path / "outputs"
            
            video_file.touch()
            audio_file.touch()
            output_dir.mkdir()
            
            yield {
                "video": str(video_file),
                "audio": str(audio_file),
                "output_dir": str(output_dir)
            }
    
    def test_package_import(self):
        """Test that all main classes can be imported."""
        from video_transcription import (
            VideoTranscriber,
            SpeakerIdentifier, 
            TranscriptFormatter,
            VideoTranscriptionPipeline,
            BatchProcessor
        )
        
        # Test instantiation
        transcriber = VideoTranscriber()
        identifier = SpeakerIdentifier()
        formatter = TranscriptFormatter()
        pipeline = VideoTranscriptionPipeline()
        processor = BatchProcessor()
        
        assert all([transcriber, identifier, formatter, pipeline, processor])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
