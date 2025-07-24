<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Video Transcription Pro - Copilot Instructions

## Project Overview
This is a professional Python package for video transcription with GPU acceleration. The package combines OpenAI Whisper for speech recognition with PyAnnote Audio for speaker diarization to achieve 95%+ speaker identification accuracy.

## Key Technologies
- **OpenAI Whisper**: Speech-to-text transcription with GPU acceleration
- **PyAnnote Audio**: Neural speaker diarization for speaker identification
- **PyTorch**: GPU acceleration and deep learning framework
- **FFmpeg**: Video/audio processing and format conversion
- **HuggingFace**: Model hosting and authentication

## Package Structure
```
src/video_transcription/
├── __init__.py              # Package initialization and exports
├── transcriber.py           # VideoTranscriber class for Whisper integration
├── speaker_identifier.py   # SpeakerIdentifier class for speaker diarization
├── formatter.py            # TranscriptFormatter class for output formatting
├── pipeline.py             # VideoTranscriptionPipeline for complete workflows
└── batch_processor.py      # BatchProcessor for multiple file processing
```

## Code Style Guidelines
- Follow PEP 8 and Google-style docstrings
- Use type hints for all function parameters and return values
- Maximum line length: 88 characters (Black formatting)
- Use descriptive variable names and comprehensive error handling
- Include performance monitoring and GPU optimization

## Key Classes and Patterns

### VideoTranscriber
- Handles OpenAI Whisper integration with GPU acceleration
- Provides audio extraction from video files using FFmpeg
- Supports all Whisper models with optimized settings for accuracy
- Returns structured results with metadata and performance metrics

### SpeakerIdentifier  
- Implements multiple speaker identification methods
- Primary: PyAnnote Audio with 95%+ accuracy and GPU acceleration
- Fallback: Audio clustering for 70%+ accuracy when PyAnnote unavailable
- Requires HuggingFace authentication for PyAnnote models

### TranscriptFormatter
- Supports multiple output formats: TXT, JSON, SRT subtitles
- Provides readable, compact, and detailed formatting styles
- Calculates speaker statistics and generates comprehensive metadata
- Handles custom speaker name mapping

### VideoTranscriptionPipeline
- Combines all components into streamlined workflow
- Supports both video and audio file processing
- Configurable output formats and cleanup options
- Comprehensive error handling and progress reporting

### BatchProcessor
- Parallel processing of multiple files with configurable workers
- Recursive folder scanning with file type filtering
- Progress tracking and comprehensive batch reporting
- Fault-tolerant processing with individual file error handling

## GPU Acceleration Best Practices
- Always check `torch.cuda.is_available()` before GPU usage
- Handle device configuration for both string and torch.device objects
- Implement fallback to CPU when GPU unavailable
- Monitor GPU memory usage and provide optimization hints

## Error Handling Patterns
- Use specific exception types (FileNotFoundError, ValueError, etc.)
- Provide helpful error messages with troubleshooting hints
- Implement graceful fallbacks for optional dependencies
- Log performance metrics and processing status

## Testing Guidelines
- Write comprehensive unit tests for all public methods
- Include integration tests for complete workflows
- Mock external dependencies (file I/O, model loading)
- Test both success and error scenarios
- Validate output formats and data integrity

## Performance Considerations
- Optimize for GPU acceleration when available
- Implement efficient batch processing with parallel workers
- Monitor memory usage for large files
- Provide processing time metrics and speed factors
- Cache models and pipelines to avoid reloading

## Documentation Standards
- Include clear usage examples in docstrings
- Provide performance benchmarks and system requirements
- Document configuration options and their impact
- Include troubleshooting guides for common issues
- Maintain up-to-date API reference documentation

## Dependencies Management
- Core: torch, openai-whisper, librosa, numpy, scipy
- Optional: pyannote.audio, huggingface_hub (for best accuracy)
- Development: pytest, black, flake8, mypy, sphinx
- System: FFmpeg for audio/video processing

## When generating code, please:
1. Follow the established patterns and class structures
2. Include comprehensive error handling and logging
3. Add type hints and detailed docstrings
4. Consider GPU acceleration and performance optimization
5. Write corresponding tests for new functionality
6. Update documentation and examples as needed
7. Ensure compatibility with the existing API design
