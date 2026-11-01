#!/usr/bin/env python3
"""Render every Manim scene of one lecture and copy the videos to its assets/ folder.

Usage:
    python tools/render_manim.py 2026-2027/ece/intro-semiconductors/lectures/lecture-01 [l|m|h]

Convention: Manim files live in <lecture>/_src/ and are named scene_*.py
(l = 480p15 draft, m = 720p30 default, h = 1080p60).
Folders starting with "_" are never published by Quarto, so source code stays private.
"""
import shutil
import subprocess
import sys
from pathlib import Path

if len(sys.argv) < 2:
    sys.exit(__doc__)

lecture = Path(sys.argv[1]).resolve()
quality = sys.argv[2] if len(sys.argv) > 2 else "m"
src, assets = lecture / "_src", lecture / "assets"
media = src / "media"
assets.mkdir(exist_ok=True)

scenes = sorted(src.glob("scene_*.py"))
if not scenes:
    sys.exit(f"No scene_*.py files found in {src}")

for scene in scenes:
    subprocess.run(
        [sys.executable, "-m", "manim", f"-q{quality}", "-a",
         "--media_dir", str(media), str(scene)],
        check=True,
    )

for mp4 in media.rglob("*.mp4"):
    if "partial_movie_files" in mp4.parts:
        continue
    shutil.copy2(mp4, assets / mp4.name)
    print("copied", mp4.name, "->", assets, f"({mp4.stat().st_size/1e6:.1f} MB)")
