"""
Video Transcription Pro - Professional video transcription with GPU acceleration.

A comprehensive Python package for high-accuracy video transcription using
OpenAI Whisper and PyAnnote Audio speaker diarization.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__description__ = "Professional video transcription with GPU-accelerated Whisper and speaker diarization"

from .transcriber import VideoTranscriber
from .speaker_identifier import SpeakerIdentifier
from .formatter import TranscriptFormatter
from .pipeline import VideoTranscriptionPipeline
from .batch_processor import BatchProcessor

__all__ = [
    "VideoTranscriber",
    "SpeakerIdentifier",
    "TranscriptFormatter",
    "VideoTranscriptionPipeline",
    "BatchProcessor",
]
