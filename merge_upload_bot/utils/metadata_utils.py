import ffmpeg
import json
import os
from typing import Dict

def edit_metadata(input_file: str, output_file: str, metadata: Dict[str, str]) -> bool:
    """
    Edit metadata of a media file using ffmpeg.
    Args:
        input_file (str): Path to the input media file.
        output_file (str): Path to the output file.
        metadata (Dict[str, str]): Dictionary containing metadata fields.

    Returns:
        bool: True if metadata was edited successfully, False otherwise.
    """
    try:
        meta_args = []
        for key, value in metadata.items():
            meta_args.extend(["-metadata", f"{key}={value}"])

        (
            ffmpeg
            .input(input_file)
            .output(output_file, **{"map_metadata": "-1"})
            .global_args(*meta_args)
            .overwrite_output()
            .run()
        )
        return True
    except ffmpeg.Error as e:
        print("FFmpeg Error:", e)
        return False

def extract_metadata(input_file: str) -> Dict[str, str]:
    """
    Extract metadata from a media file.
    Args:
        input_file (str): Path to the input media file.

    Returns:
        Dict[str, str]: Extracted metadata.
    """
    try:
        probe = ffmpeg.probe(input_file)
        format_data = probe.get("format", {}).get("tags", {})
        return format_data or {}
    except ffmpeg.Error as e:
        print("FFmpeg Probe Error:", e)
        return {}

if __name__ == "__main__":
    # Example
    inp = "input.mkv"
    out = "output.mkv"
    new_meta = {
        "title": "Beast Movie",
        "artist": "Lokesh Kanagaraj",
        "comment": "Edited by the Super Bot"
    }
    success = edit_metadata(inp, out, new_meta)
    if success:
        print("✅ Metadata updated!")
    else:
        print("❌ Failed to update metadata")
