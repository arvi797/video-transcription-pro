"""
Advanced pipeline usage example for video-transcription-pro.

This example demonstrates using the complete pipeline with custom configurations.
"""

from video_transcription import VideoTranscriptionPipeline

def main():
    """Advanced pipeline example."""
    
    print("🎥 Video Transcription Pro - Advanced Pipeline Example")
    print("=" * 60)
    
    # Step 1: Configure pipeline with advanced settings
    print("🔧 Configuring advanced pipeline...")
    
    pipeline = VideoTranscriptionPipeline(
        whisper_model="large-v3",           # Highest accuracy model
        device="cuda",                      # GPU acceleration
        speaker_method="pyannote",          # Best speaker identification
        num_speakers=3,                     # Expected number of speakers
        speaker_names={                     # Custom speaker names
            'Speaker_A': 'Meeting Host',
            'Speaker_B': 'Client Representative', 
            'Speaker_C': 'Technical Lead'
        }
    )
    
    # Step 2: Process single video
    print("\n🎬 Processing single video...")
    
    video_path = "meeting_recording.mp4"  # Update this path
    
    result = pipeline.process_video(
        video_path=video_path,
        output_dir="transcripts/meeting_001/",
        output_formats=["txt", "json", "srt"],  # Multiple output formats
        cleanup_audio=True                       # Clean up temp files
    )
    
    if result['success']:
        print(f"✅ Successfully processed: {video_path}")
        print(f"📊 Accuracy: {result['summary']['accuracy']}%")
        print(f"👥 Speakers detected: {result['summary']['num_speakers']}")
        print(f"⏱️ Duration: {result['summary']['duration_minutes']:.1f} minutes")
        
        # Display speaker statistics
        print(f"\n👥 Speaker breakdown:")
        for speaker, stats in result['speaker_stats'].items():
            duration_min = stats['total_duration'] / 60
            percentage = stats['percentage']
            print(f"   {speaker}: {duration_min:.1f}min ({percentage:.1f}%)")
        
        # Show output files
        print(f"\n📁 Output files:")
        for format_type, file_path in result['output_files'].items():
            print(f"   {format_type.upper()}: {file_path}")
    
    else:
        print(f"❌ Processing failed: {result.get('error')}")
    
    # Step 3: Process audio file directly (if you already have extracted audio)
    print(f"\n🎵 Processing audio file directly...")
    
    audio_path = "interview.wav"  # Update this path
    
    audio_result = pipeline.process_audio(
        audio_path=audio_path,
        output_dir="transcripts/interview_001/",
        output_formats=["txt", "json"]
    )
    
    if audio_result['success']:
        print(f"✅ Successfully processed audio: {audio_path}")
    
    # Step 4: Display pipeline information
    print(f"\n📋 Pipeline configuration:")
    info = pipeline.get_info()
    print(f"   Model: {info['whisper_model']}")
    print(f"   Device: {info['device']}")
    print(f"   Speaker method: {info['speaker_method']}")
    print(f"   GPU available: {info['components']['transcriber']['gpu_available']}")
    
    if info['components']['transcriber']['gpu_available']:
        gpu_name = info['components']['transcriber']['gpu_name']
        print(f"   GPU: {gpu_name}")


def example_with_custom_settings():
    """Example with highly customized settings."""
    
    print("\n🎯 Custom Configuration Example")
    print("=" * 40)
    
    # Create pipeline with specific settings for podcast transcription
    podcast_pipeline = VideoTranscriptionPipeline(
        whisper_model="large-v2",           # Slightly faster than v3
        device="cuda",
        speaker_method="pyannote",
        auth_token="your_huggingface_token", # Your HF token
        num_speakers=2,                     # Podcast with 2 hosts
        speaker_names={
            'Speaker_A': 'Host 1',
            'Speaker_B': 'Host 2'
        }
    )
    
    # Process with specific output preferences
    result = podcast_pipeline.process_video(
        video_path="podcast_episode_001.mp4",
        output_dir="podcasts/episode_001/",
        output_formats=["txt", "srt"],      # Only text and subtitles
        cleanup_audio=False                 # Keep audio for later use
    )
    
    print(f"Podcast processing complete: {result['success']}")


if __name__ == "__main__":
    main()
    example_with_custom_settings()
