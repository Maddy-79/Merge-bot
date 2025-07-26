import os
import subprocess
from typing import List, Optional

def merge_videos(input_files: List[str], output_path: str) -> bool:
    """
    Merge multiple video files (same format/codec) using ffmpeg concat.
    Creates a temporary file list and runs ffmpeg.
    """
    try:
        with open("inputs.txt", "w", encoding="utf-8") as f:
            for file in input_files:
                f.write(f"file '{file}'\n")

        cmd = [
            "ffmpeg", "-f", "concat", "-safe", "0", "-i", "inputs.txt",
            "-c", "copy", output_path
        ]
        subprocess.run(cmd, check=True)
        os.remove("inputs.txt")
        return True
    except Exception as e:
        print("FFMPEG MERGE ERROR:", e)
        return False

def add_metadata(input_file: str, output_file: str, title: str = None, artist: str = None,
                 genre: str = None, comment: str = None) -> bool:
    try:
        cmd = ["ffmpeg", "-i", input_file, "-map_metadata", "-1"]

        if title:
            cmd += ["-metadata", f"title={title}"]
        if artist:
            cmd += ["-metadata", f"artist={artist}"]
        if genre:
            cmd += ["-metadata", f"genre={genre}"]
        if comment:
            cmd += ["-metadata", f"comment={comment}"]

        cmd += ["-c", "copy", output_file]
        subprocess.run(cmd, check=True)
        return True
    except Exception as e:
        print("FFMPEG METADATA ERROR:", e)
        return False

def split_by_duration(input_file: str, duration: int, output_dir: str) -> List[str]:
    """
    Split a file into chunks of `duration` seconds
    """
    output_template = os.path.join(output_dir, "part_%03d.mkv")
    try:
        cmd = ["ffmpeg", "-i", input_file, "-c", "copy",
               "-map", "0", "-segment_time", str(duration), "-f", "segment",
               output_template]
        subprocess.run(cmd, check=True)
        return [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".mkv")]
    except Exception as e:
        print("FFMPEG SPLIT ERROR:", e)
        return []

def split_by_size(input_file: str, size_mb: int, output_dir: str) -> List[str]:
    """
    Split by approximate size. Uses bitrate estimation (not perfect).
    """
    try:
        duration = get_duration(input_file)
        file_size = os.path.getsize(input_file)
        total_mb = file_size / (1024 * 1024)

        est_parts = int(total_mb // size_mb) + 1
        part_duration = int(duration / est_parts)
        return split_by_duration(input_file, part_duration, output_dir)
    except Exception as e:
        print("SPLIT BY SIZE ERROR:", e)
        return []

def get_duration(filepath: str) -> float:
    """Get video duration in seconds"""
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration", "-of",
            "default=noprint_wrappers=1:nokey=1", filepath
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return float(result.stdout)
    except Exception as e:
        print("GET DURATION ERROR:", e)
        return 0.0
