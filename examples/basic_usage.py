"""
Basic usage example for video-transcription-pro.

This example demonstrates the simplest way to transcribe a video file
with speaker identification.
"""

from video_transcription import VideoTranscriber, SpeakerIdentifier, TranscriptFormatter

def main():
    """Basic transcription example."""
    
    # Configure your video file path
    video_path = "your_video.mp4"  # Update this path
    
    print("🎥 Video Transcription Pro - Basic Example")
    print("=" * 50)
    
    # Step 1: Initialize components
    print("🔧 Initializing components...")
    transcriber = VideoTranscriber(model="large-v3", device="cuda")
    speaker_identifier = SpeakerIdentifier()
    formatter = TranscriptFormatter()
    
    # Step 2: Extract audio from video
    print(f"🎵 Extracting audio from: {video_path}")
    audio_path = transcriber.extract_audio(video_path)
    
    # Step 3: Transcribe speech
    print("🎤 Transcribing speech...")
    whisper_result = transcriber.transcribe(audio_path)
    
    # Step 4: Identify speakers
    print("🎭 Identifying speakers...")
    speaker_result = speaker_identifier.identify_speakers(
        audio_path=audio_path,
        whisper_result=whisper_result,
        num_speakers=2  # Adjust based on your video
    )
    
    # Step 5: Format and save transcript
    print("💾 Saving transcript...")
    
    # Custom speaker names (optional)
    speaker_names = {
        'Speaker_A': 'John Doe',
        'Speaker_B': 'Jane Smith'
    }
    
    # Save as readable text
    transcript_path = formatter.save_transcript(
        speaker_result, 
        "transcript.txt",
        speaker_names=speaker_names
    )
    
    # Save as JSON data
    json_path = formatter.save_json(speaker_result, "transcript_data.json")
    
    # Save as SRT subtitles
    srt_path = formatter.save_srt(speaker_result, "subtitles.srt", speaker_names)
    
    # Display summary
    print(f"\n✅ Transcription complete!")
    print(f"📄 Text transcript: {transcript_path}")
    print(f"📊 JSON data: {json_path}")
    print(f"🎬 SRT subtitles: {srt_path}")
    
    # Show preview
    segments = speaker_result.get('segments', [])
    print(f"\n📋 Preview (first 3 segments):")
    for i, segment in enumerate(segments[:3], 1):
        speaker = segment.get('speaker', 'Unknown')
        text = segment.get('text', '').strip()
        start = segment.get('start', 0)
        print(f"   {i}. [{start:.1f}s] {speaker}: {text}")
    
    if len(segments) > 3:
        print(f"   ... and {len(segments) - 3} more segments")


if __name__ == "__main__":
    main()
