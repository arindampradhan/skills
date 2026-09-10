#!/usr/bin/env python3
"""Generate local TTS narration for a browser-use recording and mux it into video.mp4.

Reads the compiled composition.js (produced by `browser-use video review`) to find
each beat's on-screen start time and narration text, synthesizes each line with the
macOS `say` command (fully local, no network calls), and muxes the result into
video.mp4 with ffmpeg, timed to match each caption.

Usage:
    narrate.py [--recording DIR] [--voice NAME] [--output PATH]

If --recording is omitted, the latest browser-use recording is used
(`browser-use recordings --latest`).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def latest_recording() -> Path:
    result = subprocess.run(
        ["browser-use", "recordings", "--latest"],
        capture_output=True, text=True, check=True,
    )
    return Path(result.stdout.strip())


def load_composition(recording: Path) -> dict:
    text = (recording / "composition.js").read_text(encoding="utf-8").strip()
    prefix = "window.COMPOSITION ="
    if not text.startswith(prefix) or not text.endswith(";"):
        raise SystemExit(f"{recording / 'composition.js'} is not a generated composition")
    return json.loads(text[len(prefix):-1].strip())


def beat_text(beat: dict) -> str | None:
    if beat.get("card"):
        parts = [beat.get("title"), beat.get("sub")]
        text = " — ".join(part for part in parts if part)
        return text or None
    return beat.get("narration")


def timed_lines(composition: dict) -> list[tuple[float, str]]:
    lines: list[tuple[float, str]] = []
    elapsed = 0.0
    for beat in composition.get("beats", []):
        text = beat_text(beat)
        if text:
            lines.append((elapsed, text))
        elapsed += float(beat.get("dur", 0))
    return lines


def video_duration(video_path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video_path)],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())


def synthesize(voice: str, text: str, out_path: Path) -> None:
    subprocess.run(["say", "-v", voice, "-o", str(out_path), text], check=True)


def mux(video_path: Path, clips: list[tuple[float, Path]], duration: float, output_path: Path) -> None:
    inputs: list[str] = ["-i", str(video_path)]
    for _, clip_path in clips:
        inputs += ["-i", str(clip_path)]

    delayed = []
    for index, (start_seconds, _) in enumerate(clips):
        ms = round(start_seconds * 1000)
        delayed.append(f"[{index + 1}:a]adelay={ms}|{ms}[a{index}]")

    mix_inputs = "".join(f"[a{index}]" for index in range(len(clips)))
    filter_complex = (
        ";".join(delayed)
        + f";{mix_inputs}amix=inputs={len(clips)}:duration=longest:dropout_transition=0,"
        f"apad=whole_dur={duration}[aout]"
    )

    command = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy", "-c:a", "aac", "-shortest",
        str(output_path),
    ]
    subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recording", type=Path, default=None, help="Recording directory (default: latest)")
    parser.add_argument("--voice", default="Serena (Premium)", help="macOS `say` voice name")
    parser.add_argument("--output", type=Path, default=None, help="Output MP4 path")
    args = parser.parse_args()

    recording = args.recording or latest_recording()
    video_path = recording / "video.mp4"
    if not video_path.is_file():
        raise SystemExit(
            f"{video_path} not found — run `browser-use video review {recording}` and "
            f"`browser-use video export {recording} --reviewed` first."
        )

    composition = load_composition(recording)
    lines = timed_lines(composition)
    if not lines:
        raise SystemExit("No narration or card text found in composition.js")

    duration = video_duration(video_path)

    narration_dir = recording / "narration"
    narration_dir.mkdir(exist_ok=True)

    clips: list[tuple[float, Path]] = []
    for index, (start_seconds, text) in enumerate(lines):
        clip_path = narration_dir / f"{index}.aiff"
        synthesize(args.voice, text, clip_path)
        clips.append((start_seconds, clip_path))
        print(f"  {start_seconds:6.2f}s  {text}")

    output_path = args.output or recording / "video-narrated.mp4"
    mux(video_path, clips, duration, output_path)
    print(f"\nnarrated video: {output_path}")


if __name__ == "__main__":
    main()
