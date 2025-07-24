"""
Batch processing example for video-transcription-pro.

This example demonstrates processing multiple video files efficiently.
"""

from video_transcription import BatchProcessor
from pathlib import Path

def main():
    """Batch processing example."""
    
    print("🎥 Video Transcription Pro - Batch Processing Example")
    print("=" * 65)
    
    # Step 1: Configure batch processor
    print("🔧 Configuring batch processor...")
    
    processor = BatchProcessor(
        whisper_model="large-v3",           # High accuracy
        device="cuda",                      # GPU acceleration
        speaker_method="pyannote",          # Best speaker identification
        max_workers=2,                      # Parallel processing
        output_formats=["txt", "json", "srt"]  # Multiple formats
    )
    
    # Step 2: Process entire folder
    print("\n📁 Processing entire folder...")
    
    input_folder = "videos/"               # Folder with video files
    output_folder = "batch_transcripts/"   # Output folder
    
    results = processor.process_folder(
        input_folder=input_folder,
        output_folder=output_folder,
        recursive=True,                     # Include subfolders
        parallel=True                       # Use parallel processing
    )
    
    # Display results summary
    successful = sum(1 for r in results if r.get('success', False))
    failed = len(results) - successful
    
    print(f"\n📊 Batch processing summary:")
    print(f"   ✅ Successful: {successful}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📁 Total files: {len(results)}")
    
    # Show details for successful files
    if successful > 0:
        print(f"\n✅ Successfully processed files:")
        for result in results:
            if result.get('success'):
                video_name = Path(result['video_path']).name
                accuracy = result['summary']['accuracy']
                speakers = result['summary']['num_speakers']
                duration = result['summary']['duration_minutes']
                print(f"   📹 {video_name}: {accuracy}% accuracy, {speakers} speakers, {duration:.1f}min")
    
    # Show failed files
    if failed > 0:
        print(f"\n❌ Failed files:")
        for result in results:
            if not result.get('success'):
                video_name = Path(result['video_path']).name
                error = result.get('error', 'Unknown error')
                print(f"   📹 {video_name}: {error}")
    
    return results


def process_specific_files():
    """Process a specific list of files."""
    
    print("\n📄 Processing specific file list...")
    
    # Configure processor for meeting recordings
    meeting_processor = BatchProcessor(
        whisper_model="large-v3",
        device="cuda",
        speaker_method="pyannote",
        max_workers=1,                      # Sequential for meetings
        output_formats=["txt", "json"]      # Text and data only
    )
    
    # List of specific files to process
    file_list = [
        "meetings/team_standup_2024_01_15.mp4",
        "meetings/client_call_2024_01_16.mp4", 
        "meetings/project_review_2024_01_17.mp4"
    ]
    
    results = meeting_processor.process_file_list(
        file_paths=file_list,
        output_folder="meeting_transcripts/",
        parallel=False  # Process meetings sequentially for consistency
    )
    
    print(f"Meeting processing complete: {len(results)} files processed")
    return results


def process_with_filtering():
    """Process only specific file types."""
    
    print("\n🎯 Processing with file type filtering...")
    
    # Process only MP4 files
    video_processor = BatchProcessor(
        whisper_model="medium",             # Faster processing
        device="cuda",
        max_workers=3                       # More parallel workers
    )
    
    results = video_processor.process_folder(
        input_folder="mixed_media/",
        output_folder="video_only_transcripts/",
        filter_extensions=[".mp4", ".mkv"],  # Only video files
        recursive=True,
        parallel=True
    )
    
    print(f"Video-only processing complete: {len(results)} files")
    
    # Process only audio files
    audio_processor = BatchProcessor(
        whisper_model="large-v3",           # High accuracy for audio
        device="cuda",
        max_workers=2
    )
    
    audio_results = audio_processor.process_folder(
        input_folder="audio_recordings/",
        output_folder="audio_transcripts/", 
        filter_extensions=[".mp3", ".wav", ".m4a"],  # Only audio files
        recursive=False,                    # Current folder only
        parallel=True
    )
    
    print(f"Audio-only processing complete: {len(audio_results)} files")
    
    return results + audio_results


def monitor_large_batch():
    """Example for monitoring large batch processing."""
    
    print("\n📊 Large batch processing with monitoring...")
    
    processor = BatchProcessor(
        whisper_model="large-v3",
        device="cuda",
        speaker_method="pyannote",
        max_workers=2,
        output_formats=["txt", "json"]
    )
    
    # Get processor info
    info = processor.get_info()
    print(f"📋 Processor configuration:")
    print(f"   Max workers: {info['max_workers']}")
    print(f"   Supported formats: {', '.join(info['supported_extensions'])}")
    print(f"   GPU available: {info['pipeline']['components']['transcriber']['gpu_available']}")
    
    # Process large folder (example)
    large_folder = "large_video_collection/"
    
    if Path(large_folder).exists():
        results = processor.process_folder(
            input_folder=large_folder,
            output_folder="large_batch_output/",
            recursive=True,
            parallel=True
        )
        
        # Detailed analysis
        total_duration = sum(
            r['summary']['duration_minutes'] 
            for r in results 
            if r.get('success') and 'summary' in r
        )
        
        print(f"\n📈 Large batch analysis:")
        print(f"   Total video duration: {total_duration:.1f} minutes")
        print(f"   Average accuracy: {sum(r['summary']['accuracy'] for r in results if r.get('success')) / len([r for r in results if r.get('success')]):.1f}%")
        
    else:
        print(f"⚠️ Large folder not found: {large_folder}")


if __name__ == "__main__":
    # Run different batch processing examples
    main_results = main()
    specific_results = process_specific_files()
    filtered_results = process_with_filtering()
    monitor_large_batch()
    
    print(f"\n🎉 All batch processing examples completed!")
    print(f"📊 Total files processed across all examples: {len(main_results) + len(specific_results) + len(filtered_results)}")
