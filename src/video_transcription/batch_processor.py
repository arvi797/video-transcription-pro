"""
Batch processing functionality for multiple video files.
"""

import concurrent.futures
from pathlib import Path
from typing import Dict, List, Optional, Union
import time

from .pipeline import VideoTranscriptionPipeline


class BatchProcessor:
    """
    Batch processing for multiple video files.

    This class enables efficient processing of multiple video files with
    parallel processing capabilities and comprehensive progress tracking.

    Attributes:
        pipeline: VideoTranscriptionPipeline instance
        max_workers: Maximum number of parallel workers
        supported_extensions: Supported video/audio file extensions

    Example:
        >>> processor = BatchProcessor(
        ...     whisper_model="large-v3",
        ...     device="cuda",
        ...     max_workers=2
        ... )
        >>> results = processor.process_folder("videos/", "transcripts/")
        >>> print(f"Processed {len(results)} files successfully")
    """

    def __init__(
        self,
        whisper_model: str = "large-v3",
        device: Optional[str] = None,
        speaker_method: Optional[str] = None,
        auth_token: Optional[str] = None,
        max_workers: int = 1,
        output_formats: List[str] = None,
    ):
        """
        Initialize the batch processor.

        Args:
            whisper_model: Whisper model name
            device: Computing device ('cuda', 'cpu', or None)
            speaker_method: Speaker identification method
            auth_token: HuggingFace authentication token
            max_workers: Maximum number of parallel processing workers
            output_formats: Default output formats for all files
        """
        self.pipeline = VideoTranscriptionPipeline(
            whisper_model=whisper_model,
            device=device,
            speaker_method=speaker_method,
            auth_token=auth_token,
        )

        self.max_workers = max_workers
        self.output_formats = output_formats or ["txt", "json"]

        # Supported file extensions
        self.supported_extensions = {
            ".mp4",
            ".mkv",
            ".avi",
            ".mov",
            ".wmv",
            ".flv",
            ".webm",  # Video
            ".mp3",
            ".wav",
            ".m4a",
            ".aac",
            ".ogg",
            ".flac",  # Audio
        }

        print(f"🔄 BatchProcessor initialized")
        print(f"👷 Max workers: {max_workers}")
        print(f"📁 Output formats: {', '.join(self.output_formats)}")

    def process_folder(
        self,
        input_folder: Union[str, Path],
        output_folder: Union[str, Path],
        recursive: bool = False,
        filter_extensions: Optional[List[str]] = None,
        parallel: bool = True,
    ) -> List[Dict]:
        """
        Process all video/audio files in a folder.

        Args:
            input_folder: Path to folder containing media files
            output_folder: Path to folder for output files
            recursive: Whether to search subfolders recursively
            filter_extensions: Specific extensions to process (optional)
            parallel: Whether to use parallel processing

        Returns:
            List of processing results for each file

        Raises:
            FileNotFoundError: If input folder doesn't exist
        """
        input_folder = Path(input_folder)
        output_folder = Path(output_folder)

        if not input_folder.exists():
            raise FileNotFoundError(f"Input folder not found: {input_folder}")

        output_folder.mkdir(parents=True, exist_ok=True)

        # Find media files
        media_files = self._find_media_files(
            input_folder, recursive=recursive, filter_extensions=filter_extensions
        )

        if not media_files:
            print(f"❌ No media files found in {input_folder}")
            return []

        print(f"📁 Found {len(media_files)} media files in {input_folder}")
        print(f"📤 Output folder: {output_folder}")
        print(
            f"🔄 Processing mode: {'Parallel' if parallel and self.max_workers > 1 else 'Sequential'}"
        )
        print("=" * 60)

        start_time = time.time()

        if parallel and self.max_workers > 1:
            results = self._process_parallel(media_files, output_folder)
        else:
            results = self._process_sequential(media_files, output_folder)

        end_time = time.time()
        processing_time = end_time - start_time

        # Generate summary
        successful = sum(1 for r in results if r.get("success", False))
        failed = len(results) - successful

        print(f"\n📊 BATCH PROCESSING COMPLETE")
        print(f"✅ Successful: {successful}/{len(results)}")
        print(f"❌ Failed: {failed}")
        print(f"⏱️ Total time: {processing_time/60:.1f} minutes")
        print(f"📁 Results saved to: {output_folder}")

        # Save batch summary
        self._save_batch_summary(results, output_folder, processing_time)

        return results

    def process_file_list(
        self,
        file_paths: List[Union[str, Path]],
        output_folder: Union[str, Path],
        parallel: bool = True,
    ) -> List[Dict]:
        """
        Process a specific list of files.

        Args:
            file_paths: List of file paths to process
            output_folder: Path to folder for output files
            parallel: Whether to use parallel processing

        Returns:
            List of processing results for each file
        """
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)

        # Validate files exist
        valid_files = []
        for file_path in file_paths:
            file_path = Path(file_path)
            if file_path.exists():
                valid_files.append(file_path)
            else:
                print(f"⚠️ File not found: {file_path}")

        if not valid_files:
            print("❌ No valid files to process")
            return []

        print(f"📄 Processing {len(valid_files)} files")
        print(f"📤 Output folder: {output_folder}")

        if parallel and self.max_workers > 1:
            return self._process_parallel(valid_files, output_folder)
        else:
            return self._process_sequential(valid_files, output_folder)

    def _find_media_files(
        self,
        folder: Path,
        recursive: bool = False,
        filter_extensions: Optional[List[str]] = None,
    ) -> List[Path]:
        """Find all media files in a folder."""
        extensions_to_use = (
            set(filter_extensions) if filter_extensions else self.supported_extensions
        )
        extensions_to_use = {ext.lower() for ext in extensions_to_use}

        media_files = []

        if recursive:
            pattern = "**/*"
        else:
            pattern = "*"

        for file_path in folder.glob(pattern):
            if file_path.is_file() and file_path.suffix.lower() in extensions_to_use:
                media_files.append(file_path)

        return sorted(media_files)

    def _process_sequential(
        self, file_paths: List[Path], output_folder: Path
    ) -> List[Dict]:
        """Process files sequentially."""
        results = []

        for i, file_path in enumerate(file_paths, 1):
            print(f"\n🎬 Processing {i}/{len(file_paths)}: {file_path.name}")

            try:
                # Create subfolder for this file's outputs
                file_output_dir = output_folder / file_path.stem

                result = self.pipeline.process_video(
                    video_path=file_path,
                    output_dir=file_output_dir,
                    output_formats=self.output_formats,
                )

                result["file_index"] = i
                result["total_files"] = len(file_paths)

                if result.get("success"):
                    print(f"✅ Completed: {file_path.name}")
                else:
                    print(f"❌ Failed: {file_path.name}")

                results.append(result)

            except Exception as e:
                print(f"❌ Error processing {file_path.name}: {e}")
                results.append(
                    {
                        "success": False,
                        "error": str(e),
                        "video_path": str(file_path),
                        "file_index": i,
                        "total_files": len(file_paths),
                    }
                )

        return results

    def _process_parallel(
        self, file_paths: List[Path], output_folder: Path
    ) -> List[Dict]:
        """Process files in parallel."""
        results = []

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            # Submit all tasks
            future_to_file = {}
            for i, file_path in enumerate(file_paths, 1):
                file_output_dir = output_folder / file_path.stem

                future = executor.submit(
                    self._process_single_file,
                    file_path,
                    file_output_dir,
                    i,
                    len(file_paths),
                )
                future_to_file[future] = file_path

            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    result = future.result()
                    results.append(result)

                    if result.get("success"):
                        print(f"✅ Completed: {file_path.name}")
                    else:
                        print(f"❌ Failed: {file_path.name}")

                except Exception as e:
                    print(f"❌ Error processing {file_path.name}: {e}")
                    results.append(
                        {
                            "success": False,
                            "error": str(e),
                            "video_path": str(file_path),
                        }
                    )

        # Sort results by file index to maintain order
        results.sort(key=lambda x: x.get("file_index", 0))
        return results

    def _process_single_file(
        self, file_path: Path, output_dir: Path, file_index: int, total_files: int
    ) -> Dict:
        """Process a single file (for parallel execution)."""
        try:
            result = self.pipeline.process_video(
                video_path=file_path,
                output_dir=output_dir,
                output_formats=self.output_formats,
            )

            result["file_index"] = file_index
            result["total_files"] = total_files

            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "video_path": str(file_path),
                "file_index": file_index,
                "total_files": total_files,
            }

    def _save_batch_summary(
        self, results: List[Dict], output_folder: Path, processing_time: float
    ) -> None:
        """Save a summary of the batch processing results."""
        import json
        from datetime import datetime

        successful_results = [r for r in results if r.get("success", False)]
        failed_results = [r for r in results if not r.get("success", False)]

        summary = {
            "batch_summary": {
                "total_files": len(results),
                "successful": len(successful_results),
                "failed": len(failed_results),
                "total_processing_time_minutes": processing_time / 60,
                "timestamp": datetime.now().isoformat(),
            },
            "pipeline_config": self.pipeline.get_info(),
            "successful_files": successful_results,
            "failed_files": [
                {"video_path": r.get("video_path"), "error": r.get("error")}
                for r in failed_results
            ],
        }

        summary_path = (
            output_folder
            / f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        print(f"📊 Batch summary saved: {summary_path}")

    def get_info(self) -> Dict:
        """
        Get batch processor configuration information.

        Returns:
            Dictionary with batch processor configuration
        """
        return {
            "max_workers": self.max_workers,
            "output_formats": self.output_formats,
            "supported_extensions": list(self.supported_extensions),
            "pipeline": self.pipeline.get_info(),
        }
