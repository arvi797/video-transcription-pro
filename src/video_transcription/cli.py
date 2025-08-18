"""
Command-line interface for video-transcription-pro.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .pipeline import VideoTranscriptionPipeline
from .batch_processor import BatchProcessor


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="video-transcribe",
        description="Professional video transcription with GPU acceleration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Transcribe single video
  video-transcribe video.mp4 -o transcripts/

  # Batch process folder  
  video-transcribe --batch videos/ -o batch_output/

  # High accuracy with GPU
  video-transcribe video.mp4 --model large-v3 --device cuda --speakers 2

  # Multiple output formats
  video-transcribe video.mp4 -f txt json srt
        """,
    )

    # Input arguments
    parser.add_argument(
        "input", help="Input video file or folder (for batch processing)"
    )

    # Output arguments
    parser.add_argument(
        "-o",
        "--output",
        help="Output directory (default: ./transcripts)",
        default="./transcripts",
    )

    parser.add_argument(
        "-f",
        "--formats",
        nargs="+",
        choices=["txt", "json", "srt"],
        default=["txt", "json"],
        help="Output formats (default: txt json)",
    )

    # Model configuration
    parser.add_argument(
        "--model",
        choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
        default="large-v3",
        help="Whisper model (default: large-v3)",
    )

    parser.add_argument(
        "--device",
        choices=["auto", "cuda", "cpu"],
        default="auto",
        help="Computing device (default: auto)",
    )

    # Speaker identification
    parser.add_argument(
        "--speakers",
        type=int,
        help="Expected number of speakers (auto-detect if not specified)",
    )

    parser.add_argument(
        "--speaker-method",
        choices=["auto", "pyannote", "clustering"],
        default="auto",
        help="Speaker identification method (default: auto)",
    )

    parser.add_argument("--speaker-names", help="JSON file with speaker name mappings")

    # Batch processing
    parser.add_argument(
        "--batch", action="store_true", help="Process entire folder (batch mode)"
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of parallel workers for batch processing (default: 1)",
    )

    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Search subfolders recursively in batch mode",
    )

    # Other options
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Delete temporary audio files after processing",
    )

    parser.add_argument(
        "--auth-token", help="HuggingFace authentication token for PyAnnote"
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    args = parser.parse_args()

    # Validate input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input path not found: {input_path}")
        sys.exit(1)

    # Process device argument
    device = None if args.device == "auto" else args.device

    # Process speaker method
    speaker_method = None if args.speaker_method == "auto" else args.speaker_method

    # Load speaker names if provided
    speaker_names = None
    if args.speaker_names:
        try:
            import json

            with open(args.speaker_names, "r") as f:
                speaker_names = json.load(f)
        except Exception as e:
            print(f"Error loading speaker names: {e}")
            sys.exit(1)

    try:
        if args.batch:
            # Batch processing mode
            print(f"🔄 Batch processing: {input_path}")

            processor = BatchProcessor(
                whisper_model=args.model,
                device=device,
                speaker_method=speaker_method,
                auth_token=args.auth_token,
                max_workers=args.workers,
                output_formats=args.formats,
            )

            results = processor.process_folder(
                input_folder=input_path,
                output_folder=args.output,
                recursive=args.recursive,
                parallel=args.workers > 1,
            )

            # Print summary
            successful = sum(1 for r in results if r.get("success", False))
            print(
                f"\n✅ Batch processing complete: {successful}/{len(results)} files successful"
            )

        else:
            # Single file processing mode
            print(f"🎬 Processing: {input_path}")

            pipeline = VideoTranscriptionPipeline(
                whisper_model=args.model,
                device=device,
                speaker_method=speaker_method,
                auth_token=args.auth_token,
                num_speakers=args.speakers,
                speaker_names=speaker_names,
            )

            result = pipeline.process_video(
                video_path=input_path,
                output_dir=args.output,
                output_formats=args.formats,
                cleanup_audio=args.cleanup,
            )

            if result["success"]:
                print(f"\n✅ Processing complete!")
                print(f"📁 Output files: {list(result['output_files'].values())}")
                print(f"📊 Accuracy: {result['summary']['accuracy']}%")
                print(f"👥 Speakers: {result['summary']['num_speakers']}")
            else:
                print(f"\n❌ Processing failed: {result.get('error')}")
                sys.exit(1)

    except KeyboardInterrupt:
        print("\n🛑 Processing interrupted by user")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
