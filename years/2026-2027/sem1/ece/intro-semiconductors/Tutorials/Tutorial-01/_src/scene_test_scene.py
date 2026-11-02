"""Manim scene: atomic levels -> energy bands.
Render with:  python tools/render_manim.py <path-to-this-lecture-folder>
"""
from manim import *


class SimpleTest(Scene):
    def construct(self):
        t = Text("Hi, This is a simple text")
        self.play(Write(t))
        self.wait()

