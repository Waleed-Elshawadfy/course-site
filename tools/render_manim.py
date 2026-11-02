#!/usr/bin/env python3
"""Render Manim scenes of one lecture and copy the videos to its assets/ folder.

Usage:
    python tools/render_manim.py <lecture> [l|m|h] [--scene scene_name.py]
    ex: python tools/render_manim.py "years\2026-2027\sem1\ece\intro-semiconductors\Tutorials\Tutorial-01" m --scene scene_band_formation.py

Convention: Manim files live in <lecture>/_src/ and are named scene_*.py
(l = 480p15 draft, m = 720p30 default, h = 1080p60). Use --scene to render
only one source file; without it, all scene_*.py files are rendered.
Folders starting with "_" are never published by Quarto, so source code stays private.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

QUALITY_DIRS = {"l": "480p15", "m": "720p30", "h": "1080p60"}


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("lecture", type=Path, help="lecture folder")
parser.add_argument(
    "quality", nargs="?", choices=QUALITY_DIRS, default="m",
    help="render quality (default: m)",
)
parser.add_argument(
    "--scene", help="render only this scene_*.py file from the lecture's _src folder",
)
args = parser.parse_args()

lecture = args.lecture.resolve()
quality = args.quality
src, assets = lecture / "_src", lecture / "assets"
media = src / "media"
assets.mkdir(exist_ok=True)

if args.scene:
    scene = (src / args.scene).resolve()
    if scene.parent != src.resolve() or not scene.name.startswith("scene_") or scene.suffix != ".py":
        parser.error("--scene must name a scene_*.py file directly inside the lecture's _src folder")
    if not scene.is_file():
        parser.error(f"Scene file not found: {scene}")
    scenes = [scene]
else:
    scenes = sorted(src.glob("scene_*.py"))

if not scenes:
    sys.exit(f"No scene_*.py files found in {src}")

for scene in scenes:
    output_dir = media / "videos" / scene.stem / QUALITY_DIRS[quality]
    previous_outputs = {
        mp4: (mp4.stat().st_mtime_ns, mp4.stat().st_size)
        for mp4 in output_dir.glob("*.mp4")
    }

    subprocess.run(
        [sys.executable, "-m", "manim", f"-q{quality}", "-a",
         "--media_dir", str(media), str(scene)],
        check=True,
    )

    rendered_outputs = [
        mp4 for mp4 in output_dir.glob("*.mp4")
        if previous_outputs.get(mp4) != (mp4.stat().st_mtime_ns, mp4.stat().st_size)
    ]
    if not rendered_outputs:
        sys.exit(f"No newly rendered MP4 files found in {output_dir}")

    for mp4 in rendered_outputs:
        shutil.copy2(mp4, assets / mp4.name)
        print("copied", mp4.name, "->", assets, f"({mp4.stat().st_size/1e6:.1f} MB)")
