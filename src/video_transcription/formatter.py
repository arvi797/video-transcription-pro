"""
Professional transcript formatting and export functionality.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime


class TranscriptFormatter:
    """
    Professional transcript formatting and export.

    This class provides multiple output formats for transcription results,
    including human-readable transcripts, structured JSON, and subtitle formats.

    Example:
        >>> formatter = TranscriptFormatter()
        >>> transcript = formatter.format_transcript(result, include_timestamps=True)
        >>> formatter.save_transcript(result, "output.txt", speaker_names=custom_names)
    """

    def __init__(self):
        """Initialize the transcript formatter."""
        pass

    def format_transcript(
        self,
        result: Dict,
        include_timestamps: bool = True,
        speaker_names: Optional[Dict] = None,
        format_style: str = "readable",
    ) -> str:
        """
        Format transcript for readability.

        Args:
            result: Speaker identification result dictionary
            include_timestamps: Whether to include timestamps
            speaker_names: Custom mapping of speaker IDs to names
            format_style: Format style ('readable', 'compact', 'detailed')

        Returns:
            Formatted transcript string
        """
        segments = result.get("segments", [])
        if not segments:
            return "No transcript available"

        # Apply custom speaker names
        if speaker_names:
            for segment in segments:
                original_speaker = segment.get("speaker", "")
                if original_speaker in speaker_names:
                    segment["speaker"] = speaker_names[original_speaker]

        if format_style == "compact":
            return self._format_compact(segments, include_timestamps)
        elif format_style == "detailed":
            return self._format_detailed(segments, include_timestamps, result)
        else:  # readable (default)
            return self._format_readable(segments, include_timestamps)

    def _format_readable(self, segments: List[Dict], include_timestamps: bool) -> str:
        """Format transcript in readable style."""
        lines = []
        current_speaker = None

        for segment in segments:
            speaker = segment.get("speaker", "Unknown")
            text = segment.get("text", "").strip()
            start_time = segment.get("start", 0)

            if not text:
                continue

            # New speaker section
            if speaker != current_speaker:
                if lines:  # Add spacing between speakers
                    lines.append("")

                if include_timestamps:
                    timestamp = self._format_timestamp(start_time)
                    lines.append(f"**{speaker}** {timestamp}:")
                else:
                    lines.append(f"**{speaker}**:")

                current_speaker = speaker

            lines.append(text)

        return "\n".join(lines)

    def _format_compact(self, segments: List[Dict], include_timestamps: bool) -> str:
        """Format transcript in compact style."""
        lines = []

        for segment in segments:
            speaker = segment.get("speaker", "Unknown")
            text = segment.get("text", "").strip()
            start_time = segment.get("start", 0)

            if not text:
                continue

            if include_timestamps:
                timestamp = self._format_timestamp(start_time)
                lines.append(f"{timestamp} {speaker}: {text}")
            else:
                lines.append(f"{speaker}: {text}")

        return "\n".join(lines)

    def _format_detailed(
        self, segments: List[Dict], include_timestamps: bool, result: Dict
    ) -> str:
        """Format transcript in detailed style with metadata."""
        lines = []

        # Add header with metadata
        method = result.get("method", "unknown")
        accuracy = result.get("accuracy_score", 0)
        num_speakers = result.get("num_speakers", 0)
        processing_time = result.get("processing_time", 0)

        lines.append("=" * 60)
        lines.append("VIDEO TRANSCRIPTION REPORT")
        lines.append("=" * 60)
        lines.append(f"Method: {method.upper()}")
        lines.append(f"Accuracy: {accuracy}%")
        lines.append(f"Speakers: {num_speakers}")
        lines.append(f"Processing Time: {processing_time:.1f}s")
        lines.append(f"Total Segments: {len(segments)}")
        lines.append("")
        lines.append("TRANSCRIPT:")
        lines.append("-" * 60)

        # Add formatted transcript
        current_speaker = None
        for i, segment in enumerate(segments, 1):
            speaker = segment.get("speaker", "Unknown")
            text = segment.get("text", "").strip()
            start_time = segment.get("start", 0)
            end_time = segment.get("end", 0)
            confidence = segment.get("confidence", "unknown")

            if not text:
                continue

            # New speaker section
            if speaker != current_speaker:
                if i > 1:  # Add spacing between speakers
                    lines.append("")

                lines.append(f"🎤 {speaker}")
                current_speaker = speaker

            if include_timestamps:
                timestamp = self._format_timestamp(start_time, end_time)
                lines.append(f"   {timestamp} [{confidence}] {text}")
            else:
                lines.append(f"   [{confidence}] {text}")

        return "\n".join(lines)

    def _format_timestamp(
        self, start_time: float, end_time: Optional[float] = None
    ) -> str:
        """Format timestamp(s) for display."""
        start_str = f"{int(start_time//60):02d}:{start_time%60:05.2f}"
        if end_time is not None:
            end_str = f"{int(end_time//60):02d}:{end_time%60:05.2f}"
            return f"[{start_str}-{end_str}]"
        else:
            return f"[{start_str}]"

    def save_transcript(
        self,
        result: Dict,
        output_path: Union[str, Path],
        speaker_names: Optional[Dict] = None,
        format_style: str = "readable",
        include_timestamps: bool = True,
    ) -> str:
        """
        Save formatted transcript to file.

        Args:
            result: Speaker identification result dictionary
            output_path: Path for output file
            speaker_names: Custom mapping of speaker IDs to names
            format_style: Format style ('readable', 'compact', 'detailed')
            include_timestamps: Whether to include timestamps

        Returns:
            Path to saved file
        """
        transcript = self.format_transcript(
            result,
            include_timestamps=include_timestamps,
            speaker_names=speaker_names,
            format_style=format_style,
        )

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcript)

        print(f"💾 Transcript saved: {output_path}")
        return str(output_path)

    def save_json(
        self, result: Dict, output_path: Union[str, Path], include_metadata: bool = True
    ) -> str:
        """
        Save results as structured JSON.

        Args:
            result: Speaker identification result dictionary
            output_path: Path for output JSON file
            include_metadata: Whether to include processing metadata

        Returns:
            Path to saved JSON file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Prepare data for JSON export
        export_data = {
            "segments": result.get("segments", []),
            "speaker_stats": self._calculate_speaker_stats(result),
            "summary": {
                "total_segments": len(result.get("segments", [])),
                "num_speakers": result.get("num_speakers", 0),
                "total_duration": self._calculate_total_duration(result),
                "method": result.get("method", "unknown"),
                "accuracy_score": result.get("accuracy_score", 0),
                "confidence": result.get("confidence", "unknown"),
            },
        }

        if include_metadata:
            export_data["metadata"] = {
                "processing_time": result.get("processing_time", 0),
                "device": result.get("device", "unknown"),
                "export_timestamp": datetime.now().isoformat(),
            }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        print(f"📊 JSON data saved: {output_path}")
        return str(output_path)

    def save_srt(
        self,
        result: Dict,
        output_path: Union[str, Path],
        speaker_names: Optional[Dict] = None,
    ) -> str:
        """
        Save as SRT subtitle format.

        Args:
            result: Speaker identification result dictionary
            output_path: Path for output SRT file
            speaker_names: Custom mapping of speaker IDs to names

        Returns:
            Path to saved SRT file
        """
        segments = result.get("segments", [])
        if not segments:
            raise ValueError("No segments found in result")

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        lines = []
        for i, segment in enumerate(segments, 1):
            speaker = segment.get("speaker", "Unknown")
            text = segment.get("text", "").strip()
            start_time = segment.get("start", 0)
            end_time = segment.get("end", 0)

            if not text:
                continue

            # Apply custom speaker names
            if speaker_names and speaker in speaker_names:
                speaker = speaker_names[speaker]

            # Format timestamps for SRT
            start_srt = self._seconds_to_srt_time(start_time)
            end_srt = self._seconds_to_srt_time(end_time)

            lines.append(str(i))
            lines.append(f"{start_srt} --> {end_srt}")
            lines.append(f"{speaker}: {text}")
            lines.append("")  # Empty line between subtitles

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"🎬 SRT subtitles saved: {output_path}")
        return str(output_path)

    def _seconds_to_srt_time(self, seconds: float) -> str:
        """Convert seconds to SRT timestamp format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

    def _calculate_speaker_stats(self, result: Dict) -> Dict:
        """Calculate statistics for each speaker."""
        segments = result.get("segments", [])
        speaker_stats = {}

        for segment in segments:
            speaker = segment.get("speaker", "Unknown")
            duration = segment.get("end", 0) - segment.get("start", 0)
            text = segment.get("text", "")

            if speaker not in speaker_stats:
                speaker_stats[speaker] = {
                    "total_duration": 0,
                    "segment_count": 0,
                    "word_count": 0,
                    "percentage": 0,
                }

            speaker_stats[speaker]["total_duration"] += duration
            speaker_stats[speaker]["segment_count"] += 1
            speaker_stats[speaker]["word_count"] += len(text.split())

        # Calculate percentages
        total_duration = sum(
            stats["total_duration"] for stats in speaker_stats.values()
        )
        for speaker, stats in speaker_stats.items():
            if total_duration > 0:
                stats["percentage"] = (stats["total_duration"] / total_duration) * 100

        return speaker_stats

    def _calculate_total_duration(self, result: Dict) -> float:
        """Calculate total duration from segments."""
        segments = result.get("segments", [])
        if not segments:
            return 0.0
        return segments[-1].get("end", 0)
