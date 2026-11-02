"""Manim scene: atomic levels -> energy bands.
Render with:  python tools/render_manim.py <path-to-this-lecture-folder>
"""
from manim import *


class BandFormation(Scene):
    def construct(self):
        n = 8                                  # number of "atoms"
        upper_y, lower_y = 1.4, -1.4

        title = Text("From atomic levels to energy bands", font_size=34).to_edge(UP)
        axis = Arrow(LEFT * 5.5 + DOWN * 2.6, LEFT * 5.5 + UP * 1.9, buff=0, color=GREY_B)
        axis_label = Text("Energy", font_size=24).next_to(axis, DOWN, buff=0.1)

        def level(y, color):
            return Line(LEFT * 1.5, RIGHT * 1.5, color=color).move_to([0, y, 0])

        def split(y, color, spread=0.9):
            return VGroup(*[
                Line(LEFT * 1.5, RIGHT * 1.5, color=color)
                .move_to([0, y + spread * (i / (n - 1) - 0.5), 0])
                for i in range(n)
            ])

        upper, lower = level(upper_y, BLUE), level(lower_y, GREEN)
        caption = Text("One atom: discrete energy levels", font_size=26).to_edge(DOWN)

        self.play(Write(title), Create(axis), FadeIn(axis_label))
        self.play(Create(upper), Create(lower), FadeIn(caption))
        self.wait(1)

        upper_split, lower_split = split(upper_y, BLUE), split(lower_y, GREEN)
        caption2 = Text("N atoms in a crystal: levels split and merge into bands",
                        font_size=26).to_edge(DOWN)
        self.play(
            ReplacementTransform(upper, upper_split),
            ReplacementTransform(lower, lower_split),
            Transform(caption, caption2),
        )
        self.wait(1)

        cb = Rectangle(width=3, height=1.0, color=BLUE, fill_opacity=0.35).move_to([0, upper_y, 0])
        vb = Rectangle(width=3, height=1.0, color=GREEN, fill_opacity=0.35).move_to([0, lower_y, 0])
        cb_label = Text("Conduction band", font_size=24, color=BLUE).next_to(cb, RIGHT)
        vb_label = Text("Valence band", font_size=24, color=GREEN).next_to(vb, RIGHT)
        self.play(FadeIn(cb), FadeIn(vb), FadeIn(cb_label), FadeIn(vb_label))

        brace = BraceBetweenPoints([-1.7, lower_y + 0.5, 0], [-1.7, upper_y - 0.5, 0], direction=LEFT)
        gap = Text("Band gap Eg", font_size=24, color=YELLOW).next_to(brace, LEFT)
        self.play(GrowFromCenter(brace), FadeIn(gap))
        self.wait(2)


class SimpleTest(Scene):
    def construct(self):
        t = Text("Hi, This is a simple text")
        self.play(Write(t))
        self.wait()

