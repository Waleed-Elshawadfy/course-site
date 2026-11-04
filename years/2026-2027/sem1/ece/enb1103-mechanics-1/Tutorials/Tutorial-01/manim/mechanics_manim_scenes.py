from manim import *
import numpy as np


class Hibbeler3DScene(ThreeDScene):
    """
    Base 3D Scene configured with standard Engineering Mechanics (Hibbeler)
    perspective: +x (bottom-left), +y (right), +z (up).
    Uses fast 2D Arrow/Line/Dot primitives and shifts the 3D axes downward
    and slightly right so the +z axis is never cut off and never overlaps the HUD.
    """

    def setup_hibbeler_axes(
        self,
        x_range=(-5, 5, 1),
        y_range=(-5, 5, 1),
        z_range=(-5, 5, 1),
        x_length=5.0,
        y_length=5.0,
        z_length=4.2,
        phi=65 * DEGREES,
        theta=30 * DEGREES,
        origin_shift=np.array([-0.6, 0.9, -1.3]),
    ):
        self.set_camera_orientation(phi=phi, theta=theta)
        axes = ThreeDAxes(
            x_range=x_range,
            y_range=y_range,
            z_range=z_range,
            x_length=x_length,
            y_length=y_length,
            z_length=z_length,
            axis_config={
                "include_tip": True,
                "color": BLUE_B,
                "tip_width": 0.18,
                "tip_height": 0.18,
            },
        )
        # Shift axes down (-z) and right (-x, +y) in screen coordinates
        axes.shift(origin_shift)

        dx = (x_range[1] - x_range[0]) * 0.08
        dy = (y_range[1] - y_range[0]) * 0.08
        dz = (z_range[1] - z_range[0]) * 0.08

        x_label = MathTex("x", color=BLUE_B).scale(0.75)
        y_label = MathTex("y", color=BLUE_B).scale(0.75)
        z_label = MathTex("z", color=BLUE_B).scale(0.75)

        x_label.move_to(axes.c2p(x_range[1] + dx, 0, 0))
        y_label.move_to(axes.c2p(0, y_range[1] + dy, 0))
        z_label.move_to(axes.c2p(0, 0, z_range[1] + dz))

        self.add_fixed_orientation_mobjects(x_label, y_label, z_label)
        return axes, VGroup(x_label, y_label, z_label)

    def create_parallelepiped(self, axes, p1, p2, color=RED_B):
        """Creates the 12 dashed edges of a 3D bounding box between p1 and p2."""
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        corners = [
            (x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1),
            (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2),
        ]
        edges_idx = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7),
        ]
        lines = VGroup()
        for i, j in edges_idx:
            lines.add(
                DashedLine(
                    axes.c2p(*corners[i]),
                    axes.c2p(*corners[j]),
                    color=color,
                    dash_length=0.08,
                    stroke_width=2.0,
                    stroke_opacity=0.65,
                )
            )
        return lines

    def arrow3d(self, axes, start, end, color=RED, stroke_width=5.0):
        """
        Fast-rendering 2D Arrow placed in 3D space (replaces slow Arrow3D mesh).
        """
        return Arrow(
            start=axes.c2p(*start),
            end=axes.c2p(*end),
            color=color,
            buff=0,
            stroke_width=stroke_width,
            max_tip_length_to_length_ratio=0.18,
            max_stroke_width_to_length_ratio=8.0,
        )

    def add_hud(self, tex_strings, corner=UL, scale=0.52, color=WHITE, shift_vec=ORIGIN):
        """
        Compact fixed-in-frame equation panel that stays clear of 3D axes and titles.
        """
        group = VGroup(*[MathTex(s, color=color).scale(scale) for s in tex_strings])
        group.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        bg = SurroundingRectangle(
            group,
            color=GRAY_D,
            fill_color=BLACK,
            fill_opacity=0.82,
            buff=0.14,
            corner_radius=0.08,
            stroke_width=1.5,
        )
        panel = VGroup(bg, group).to_corner(corner, buff=0.22).shift(shift_vec)
        self.add_fixed_in_frame_mobjects(panel)
        return panel


# ==============================================================================
# PART 1: CONCEPT & HANDWRITTEN SUMMARY SCENES (SCENES 01 - 04)
# ==============================================================================

class Scene01_2Dvs3DRightHandRule(Hibbeler3DScene):
    """
    Handwritten Summary p. 1 (top) & Lecture Fig. 2-21:
    2D Rectangular resolution vs. 3D Right-Hand Rule.
    """

    def construct(self):
        # 1. 2D Rectangular Review (No overlap between title and HUD)
        title = (
            Text("2D vs. 3D Rectangular Coordinate Systems", font_size=24, color=BLUE_A)
            .to_corner(UL, buff=0.25)
        )
        self.add_fixed_in_frame_mobjects(title)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)

        plane = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 4, 1],
            x_length=4.6,
            y_length=3.6,
            axis_config={"include_tip": True, "tip_width": 0.18, "tip_height": 0.18},
        ).shift(LEFT * 2.4 + DOWN * 0.65)

        vec_2d = Arrow(plane.c2p(0, 0), plane.c2p(3.5, 2.5), buff=0, color=RED, stroke_width=5)
        ax_line = DashedLine(plane.c2p(3.5, 0), plane.c2p(3.5, 2.5), color=YELLOW)
        ay_line = DashedLine(plane.c2p(0, 2.5), plane.c2p(3.5, 2.5), color=GREEN)
        lbl_A = MathTex(r"\mathbf{A}", color=RED).scale(0.75).next_to(vec_2d.get_end(), UR, buff=0.1)
        lbl_Ax = MathTex(r"A_x = A\cos\theta", color=YELLOW).scale(0.65).next_to(plane.c2p(1.75, 0), DOWN, buff=0.18)
        lbl_Ay = MathTex(r"A_y = A\sin\theta", color=GREEN).scale(0.65).next_to(plane.c2p(0, 1.25), LEFT, buff=0.18)

        hud_2d = self.add_hud(
            [
                r"A_x = A\cos\theta, \quad A_y = A\sin\theta",
                r"|\mathbf{A}| = \sqrt{A_x^2 + A_y^2}",
                r"\theta = \tan^{-1}(A_y / A_x)",
            ],
            corner=UR,
            shift_vec=DOWN * 0.6,
        )

        self.play(Create(plane), GrowArrow(vec_2d), Write(lbl_A))
        self.play(Create(ax_line), Create(ay_line), Write(lbl_Ax), Write(lbl_Ay))
        self.wait(1.5)

        self.play(
            FadeOut(VGroup(plane, vec_2d, ax_line, ay_line, lbl_A, lbl_Ax, lbl_Ay, hud_2d, title))
        )
        self.remove(hud_2d, title)

        # 2. Transition to 3D Right-Hand Rule (Lowered axes, HUD in UL)
        axes, labels = self.setup_hibbeler_axes(
            x_range=(-3, 4, 1), y_range=(-3, 4, 1), z_range=(-2, 4, 1)
        )
        self.play(Create(axes), FadeIn(labels))

        curl_arc = ParametricFunction(
            lambda t: axes.c2p(2.2 * np.cos(t), 2.2 * np.sin(t), 0),
            t_range=[0, PI / 2],
            color=YELLOW,
            stroke_width=4,
        )
        z_thumb = self.arrow3d(axes, (0, 0, 0), (0, 0, 3), color=GREEN, stroke_width=6)

        self.add_hud(
            [
                r"\text{Right-Handed System (Correct):}",
                r"\text{Fingers curl } +x \to +y",
                r"\text{Thumb points along } +z",
            ],
            corner=UL,
        )

        self.play(Create(curl_arc), GrowArrow(z_thumb))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()


class Scene02_CartesianParallelepiped(Hibbeler3DScene):
    """
    Handwritten Summary p. 1 (bottom) & Lecture Figs. 2-22, 2-24:
    3D Rectangular components, intermediate projection A', unit vectors i, j, k, and magnitude.
    """

    def construct(self):
        axes, labels = self.setup_hibbeler_axes(
            x_range=(0, 5, 1), y_range=(0, 5, 1), z_range=(0, 5, 1)
        )
        self.add(axes, labels)

        Ax, Ay, Az = 3.0, 3.5, 3.0
        box = self.create_parallelepiped(axes, (0, 0, 0), (Ax, Ay, Az), color=RED_B)

        vec_Ax = self.arrow3d(axes, (0, 0, 0), (Ax, 0, 0), color=BLUE)
        vec_Ay = self.arrow3d(axes, (0, 0, 0), (0, Ay, 0), color=BLUE)
        vec_Az = self.arrow3d(axes, (0, 0, 0), (0, 0, Az), color=BLUE)
        vec_A_prime = self.arrow3d(axes, (0, 0, 0), (Ax, Ay, 0), color=GREEN)
        vec_A = self.arrow3d(axes, (0, 0, 0), (Ax, Ay, Az), color=RED, stroke_width=6)

        # Unit vectors i, j, k
        vec_i = self.arrow3d(axes, (0, 0, 0), (1.2, 0, 0), color=YELLOW, stroke_width=5.5)
        vec_j = self.arrow3d(axes, (0, 0, 0), (0, 1.2, 0), color=YELLOW, stroke_width=5.5)
        vec_k = self.arrow3d(axes, (0, 0, 0), (0, 0, 1.2), color=YELLOW, stroke_width=5.5)

        self.add_hud(
            [
                r"\mathbf{A}' = \mathbf{A}_x + \mathbf{A}_y",
                r"\mathbf{A} = A_x\mathbf{i} + A_y\mathbf{j} + A_z\mathbf{k}",
                r"|\mathbf{A}| = \sqrt{A_x^2 + A_y^2 + A_z^2}",
            ],
            corner=UL,
        )

        self.play(Create(box))
        self.play(GrowArrow(vec_Ax), GrowArrow(vec_Ay), GrowArrow(vec_A_prime))
        self.play(GrowArrow(vec_Az), GrowArrow(vec_A))
        self.play(GrowArrow(vec_i), GrowArrow(vec_j), GrowArrow(vec_k))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()


class Scene03_DirectionCosinesAndUnitVector(Hibbeler3DScene):
    """
    Handwritten Summary p. 2 (top) & Lecture Fig. 2-26:
    Coordinate direction angles (alpha, beta, gamma), A' = A sin(gamma), and unit vector u_A.
    """

    def construct(self):
        axes, labels = self.setup_hibbeler_axes(
            x_range=(0, 5, 1), y_range=(0, 5, 1), z_range=(0, 5, 1)
        )
        self.add(axes, labels)

        vec = np.array([2.5, 3.0, 3.2])
        norm = np.linalg.norm(vec)
        unit_v = vec / norm

        box = self.create_parallelepiped(axes, (0, 0, 0), tuple(vec), color=GRAY)
        arrow_A = self.arrow3d(axes, (0, 0, 0), tuple(vec), color=RED, stroke_width=6)
        arrow_uA = self.arrow3d(axes, (0, 0, 0), tuple(unit_v * 1.6), color=YELLOW, stroke_width=6.5)
        arrow_Aprime = self.arrow3d(axes, (0, 0, 0), (vec[0], vec[1], 0), color=GREEN, stroke_width=4)

        self.add_hud(
            [
                r"\cos\alpha = \frac{A_x}{|\mathbf{A}|}, \; \cos\beta = \frac{A_y}{|\mathbf{A}|}, \; \cos\gamma = \frac{A_z}{|\mathbf{A}|}",
                r"\mathbf{u}_A = \frac{\mathbf{A}}{|\mathbf{A}|} = \cos\alpha\mathbf{i} + \cos\beta\mathbf{j} + \cos\gamma\mathbf{k}",
                r"\cos^2\alpha + \cos^2\beta + \cos^2\gamma = 1, \quad A' = A\sin\gamma",
            ],
            corner=UL,
        )

        self.play(Create(box), GrowArrow(arrow_A))
        self.play(GrowArrow(arrow_Aprime), GrowArrow(arrow_uA))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3.5)
        self.stop_ambient_camera_rotation()


class Scene04_PositionVectors(Hibbeler3DScene):
    """
    Handwritten Summary p. 2 (bottom) & Lecture Figs. 2-34, 2-36a:
    Coordinates of A(4, 2, -6) and B(6, -1, 4), and position vector r_AB = r_B - r_A.
    """

    def construct(self):
        axes, labels = self.setup_hibbeler_axes(
            x_range=(-2, 7, 2),
            y_range=(-3, 5, 2),
            z_range=(-7, 6, 2),
            x_length=4.8,
            y_length=4.8,
            z_length=4.4,
        )
        self.add(axes, labels)

        A = (4, 2, -6)
        B = (6, -1, 4)

        path_A = VMobject(color=YELLOW, stroke_width=2.5)
        path_A.set_points_as_corners([
            axes.c2p(0, 0, 0), axes.c2p(4, 0, 0), axes.c2p(4, 2, 0), axes.c2p(4, 2, -6)
        ])
        path_B = VMobject(color=GREEN, stroke_width=2.5)
        path_B.set_points_as_corners([
            axes.c2p(0, 0, 0), axes.c2p(6, 0, 0), axes.c2p(6, -1, 0), axes.c2p(6, -1, 4)
        ])

        r_A = self.arrow3d(axes, (0, 0, 0), A, color=YELLOW)
        r_B = self.arrow3d(axes, (0, 0, 0), B, color=GREEN)
        r_AB = self.arrow3d(axes, A, B, color=RED, stroke_width=6)

        self.add_hud(
            [
                r"A(4, 2, -6)\text{ m}, \quad B(6, -1, 4)\text{ m}",
                r"\mathbf{r}_A + \mathbf{r}_{AB} = \mathbf{r}_B \implies \mathbf{r}_{AB} = \mathbf{r}_B - \mathbf{r}_A",
                r"\mathbf{r}_{AB} = (x_B - x_A)\mathbf{i} + (y_B - y_A)\mathbf{j} + (z_B - z_A)\mathbf{k}",
                r"\mathbf{r}_{AB} = 2\mathbf{i} - 3\mathbf{j} + 10\mathbf{k}\text{ m}",
            ],
            corner=UL,
        )

        self.play(Create(path_A), GrowArrow(r_A))
        self.play(Create(path_B), GrowArrow(r_B))
        self.play(GrowArrow(r_AB))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3.5)
        self.stop_ambient_camera_rotation()


# ==============================================================================
# PART 2: WORKED LECTURE EXAMPLES (SCENES 05 - 08)
# ==============================================================================

class Scene05_Example1_EyeboltCable(Hibbeler3DScene):
    """
    Lecture Example 1 (Slides 13-14):
    Cable from A(4, 0, 3) to B(0, 6, 0) pulled with F = 500 N.
    """

    def construct(self):
        axes, labels = self.setup_hibbeler_axes(
            x_range=(0, 6, 1), y_range=(0, 7, 1), z_range=(0, 5, 1)
        )
        self.add(axes, labels)

        A = (4, 0, 3)
        B = (0, 6, 0)
        box = self.create_parallelepiped(axes, (0, 0, 0), (4, 6, 3), color=GRAY)
        vec_AB = self.arrow3d(axes, A, B, color=YELLOW, stroke_width=4)
        vec_F = self.arrow3d(axes, A, (2.2, 2.7, 1.65), color=RED, stroke_width=6)

        # Component vectors at A
        Fx = self.arrow3d(axes, A, (2.0, 0, 3), color=BLUE)
        Fy = self.arrow3d(axes, A, (4, 2.8, 3), color=BLUE)
        Fz = self.arrow3d(axes, A, (4, 0, 1.5), color=BLUE)

        self.add_hud(
            [
                r"\text{Ex 1: } A(4, 0, 3)\text{ m}, \; B(0, 6, 0)\text{ m}, \; F = 500\text{ N}",
                r"\vec{AB} = -4\mathbf{i} + 6\mathbf{j} - 3\mathbf{k}\text{ m}, \quad |\vec{AB}| = \sqrt{61} \approx 7.81\text{ m}",
                r"\mathbf{u}_{AB} = -0.5122\mathbf{i} + 0.7682\mathbf{j} - 0.3841\mathbf{k}",
                r"\mathbf{F} = F\mathbf{u}_{AB} = \{-256\mathbf{i} + 384\mathbf{j} - 192\mathbf{k}\}\text{ N}",
            ],
            corner=UL,
        )

        self.play(Create(box), GrowArrow(vec_AB))
        self.play(GrowArrow(vec_F))
        self.play(GrowArrow(Fx), GrowArrow(Fy), GrowArrow(Fz))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()


class Scene06_Example2_DirectionAngles(Hibbeler3DScene):
    """
    Lecture Example 2 (Slide 15):
    F = 200 N with beta = 60 deg, gamma = 45 deg -> alpha = 60 deg.
    """

    def construct(self):
        axes, labels = self.setup_hibbeler_axes(
            x_range=(0, 4, 1), y_range=(0, 4, 1), z_range=(0, 4, 1)
        )
        self.add(axes, labels)

        F_vec = (2.0, 2.0, 2.828)
        box = self.create_parallelepiped(axes, (0, 0, 0), F_vec, color=YELLOW_B)
        arrow_F = self.arrow3d(axes, (0, 0, 0), F_vec, color=RED, stroke_width=6)

        self.add_hud(
            [
                r"\text{Ex 2: } F = 200\text{ N}, \; \beta = 60^\circ, \; \gamma = 45^\circ",
                r"\cos^2\alpha + \cos^2 60^\circ + \cos^2 45^\circ = 1 \implies \alpha = 60^\circ",
                r"\mathbf{F} = 200\cos 60^\circ\mathbf{i} + 200\cos 60^\circ\mathbf{j} + 200\cos 45^\circ\mathbf{k}",
                r"\mathbf{F} = \{100.0\mathbf{i} + 100.0\mathbf{j} + 141.4\mathbf{k}\}\text{ N}",
            ],
            corner=UL,
        )

        self.play(Create(box), GrowArrow(arrow_F))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()


class Scene07_Example3_DoubleProjection(Hibbeler3DScene):
    """
    Lecture Example 3 (Slide 16):
    Position vector A = 12 m at 30 deg from +z and 40 deg from +x in xy-plane.
    """

    def construct(self):
        axes, labels = self.setup_hibbeler_axes(
            x_range=(0, 6, 1), y_range=(0, 6, 1), z_range=(0, 6, 1)
        )
        self.add(axes, labels)

        s = 0.42
        Ax, Ay, Az = 4.596 * s, 3.857 * s, 10.392 * s
        box = self.create_parallelepiped(axes, (0, 0, 0), (Ax, Ay, Az), color=GRAY)
        vec_A = self.arrow3d(axes, (0, 0, 0), (Ax, Ay, Az), color=RED, stroke_width=6)
        vec_Axy = self.arrow3d(axes, (0, 0, 0), (Ax, Ay, 0), color=GREEN, stroke_width=4.5)

        self.add_hud(
            [
                r"\text{Ex 3: } A = 12\text{ m}, \; \theta_z = 30^\circ, \; \phi_{xy} = 40^\circ",
                r"A_z = 12\cos 30^\circ = 10.39\text{ m}, \; A_{xy} = 12\sin 30^\circ = 6\text{ m}",
                r"A_x = 6\cos 40^\circ = 4.60\text{ m}, \; A_y = 6\sin 40^\circ = 3.86\text{ m}",
                r"\theta_x = 67.5^\circ, \quad \theta_y = 71.3^\circ, \quad \theta_z = 30.0^\circ",
            ],
            corner=UL,
        )

        self.play(Create(box), GrowArrow(vec_Axy), GrowArrow(vec_A))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()


class Scene08_Example4_ObtuseAngles(Hibbeler3DScene):
    """
    Lecture Example 4 (Slide 17):
    F = 500 N in (+x, -y, -z) octant: beta = 135 deg, gamma = 120 deg, alpha = 60 deg.
    """

    def construct(self):
        axes, labels = self.setup_hibbeler_axes(
            x_range=(-1, 4, 1), y_range=(-4, 2, 1), z_range=(-4, 2, 1)
        )
        self.add(axes, labels)

        F_end = (2.5, -3.54, -2.5)
        box = self.create_parallelepiped(axes, (0, 0, 0), F_end, color=BLUE_C)
        vec_F = self.arrow3d(axes, (0, 0, 0), F_end, color=RED, stroke_width=6)

        self.add_hud(
            [
                r"\text{Ex 4: } F = 500\text{ N}, \; \beta = 135^\circ, \; \gamma = 120^\circ",
                r"\cos^2\alpha + \cos^2 135^\circ + \cos^2 120^\circ = 1 \implies \alpha = 60^\circ",
                r"\mathbf{F} = 500(0.5\mathbf{i} - 0.7071\mathbf{j} - 0.5\mathbf{k})",
                r"\mathbf{F} = \{250\mathbf{i} - 354\mathbf{j} - 250\mathbf{k}\}\text{ N}",
            ],
            corner=UL,
        )

        self.play(Create(box), GrowArrow(vec_F))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()


# ==============================================================================
# PART 3: TUTORIAL & ASSIGNMENT PROBLEMS 1 - 10 (SCENES 09 - 18)
# ==============================================================================

class Scene09_Problem1_ForceP(Hibbeler3DScene):
    """Problem 1 (Slide 18 top): Force P = 30 N at 50 deg elevation, 30 deg from +y toward -x."""

    def construct(self):
        axes, labels = self.setup_hibbeler_axes(
            x_range=(-3, 3, 1), y_range=(0, 4, 1), z_range=(0, 4, 1)
        )
        self.add(axes, labels)

        P_end = (-9.64 / 8, 16.70 / 8, 22.98 / 8)
        box = self.create_parallelepiped(axes, (0, 0, 0), P_end, color=BLUE_B)
        vec_Pxy = self.arrow3d(axes, (0, 0, 0), (P_end[0], P_end[1], 0), color=GREEN, stroke_width=4.5)
        vec_P = self.arrow3d(axes, (0, 0, 0), P_end, color=RED, stroke_width=6)

        self.add_hud(
            [
                r"\text{Prob 1: } P = 30\text{ N}, \; \phi = 50^\circ, \; 30^\circ\text{ from }+y\text{ to }-x",
                r"P_z = 30\sin 50^\circ = 22.98\text{ N}, \; P_{xy} = 30\cos 50^\circ = 19.28\text{ N}",
                r"P_x = -P_{xy}\sin 30^\circ = -9.64\text{ N}, \; P_y = P_{xy}\cos 30^\circ = 16.70\text{ N}",
                r"\mathbf{P} = \{-9.64\mathbf{i} + 16.70\mathbf{j} + 22.98\mathbf{k}\}\text{ N}",
            ],
            corner=UL,
        )

        self.play(Create(box), GrowArrow(vec_Pxy), GrowArrow(vec_P))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()


class Scene10_Problem2_BracketForce(Hibbeler3DScene):
    """Problem 2 (Slide 18 bottom): F = 400 N on bracket, beta = 60 deg, gamma = 45 deg."""

    def construct(self):
        axes, labels = self.setup_hibbeler_axes(
            x_range=(-4, 3, 1), y_range=(0, 4, 1), z_range=(0, 4, 1)
        )
        self.add(axes, labels)

        F_end = (-2.0, 2.0, 2.828)
        box = self.create_parallelepiped(axes, (0, 0, 0), F_end, color=YELLOW)
        vec_F = self.arrow3d(axes, (0, 0, 0), F_end, color=RED, stroke_width=6)

        self.add_hud(
            [
                r"\text{Prob 2: } F = 400\text{ N}, \; \beta = 60^\circ, \; \gamma = 45^\circ",
                r"\cos\alpha = \pm 0.5 \implies |F_x| = 200\text{ N}",
                r"F_y = 400\cos 60^\circ = 200\text{ N}",
                r"F_z = 400\cos 45^\circ = 282.8\text{ N}",
            ],
            corner=UL,
        )

        self.play(Create(box), GrowArrow(vec_F))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()


class Scene11_Problem3_ResultantAlongX(Hibbeler3DScene):
    """Problem 3 (Slide 19 top): F1 = 180 N and F2 with resultant F_R = 500i N."""

    def construct(self):
        axes, labels = self.setup_hibbeler_axes(
            x_range=(0, 6, 1), y_range=(-2, 3, 1), z_range=(-2, 3, 1)
        )
        self.add(axes, labels)

        F1 = (1.506, 0.869, -0.466)
        F2 = (3.494, -0.869, 0.466)
        FR = (5.0, 0, 0)

        v_F1 = self.arrow3d(axes, (0, 0, 0), F1, color=BLUE)
        v_F2 = self.arrow3d(axes, (0, 0, 0), F2, color=GREEN)
        v_FR = self.arrow3d(axes, (0, 0, 0), FR, color=RED, stroke_width=6)

        self.add_hud(
            [
                r"\text{Prob 3: } \mathbf{F}_R = \mathbf{F}_1 + \mathbf{F}_2 = 500\mathbf{i}\text{ N}",
                r"\mathbf{F}_1 = \{150.6\mathbf{i} + 86.9\mathbf{j} - 46.6\mathbf{k}\}\text{ N}",
                r"\mathbf{F}_2 = \{349.4\mathbf{i} - 86.9\mathbf{j} + 46.6\mathbf{k}\}\text{ N}",
                r"F_2 = 363.1\text{ N}, \; \alpha_2 = 15.8^\circ, \; \beta_2 = 103.9^\circ, \; \gamma_2 = 82.6^\circ",
            ],
            corner=UL,
        )

        self.play(GrowArrow(v_F1), GrowArrow(v_F2))
        self.play(GrowArrow(v_FR))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()


class Scene12_Problem4_PoleForce(Hibbeler3DScene):
    """Problem 4 (Slide 19 bottom): Pole force with Fx = 1.5 kN, Fz = 1.25 kN, beta = 75 deg."""

    def construct(self):
        axes, labels = self.setup_hibbeler_axes(
            x_range=(0, 3, 1), y_range=(0, 3, 1), z_range=(0, 3, 1)
        )
        self.add(axes, labels)

        F_end = (1.5, 0.523, 1.25)
        box = self.create_parallelepiped(axes, (0, 0, 0), F_end, color=GRAY)
        v_Fx = self.arrow3d(axes, (0, 0, 0), (1.5, 0, 0), color=BLUE)
        v_Fy = self.arrow3d(axes, (0, 0, 0), (0, 0.523, 0), color=BLUE)
        v_Fz = self.arrow3d(axes, (0, 0, 0), (0, 0, 1.25), color=BLUE)
        v_F = self.arrow3d(axes, (0, 0, 0), F_end, color=RED, stroke_width=6)

        self.add_hud(
            [
                r"\text{Prob 4: } F_x = 1.5\text{ kN}, \; F_z = 1.25\text{ kN}, \; \beta = 75^\circ",
                r"F = \frac{\sqrt{F_x^2 + F_z^2}}{\sin 75^\circ} = 2.02\text{ kN}",
                r"F_y = F\cos 75^\circ = 0.523\text{ kN}",
            ],
            corner=UL,
        )

        self.play(Create(box), GrowArrow(v_Fx), GrowArrow(v_Fz))
        self.play(GrowArrow(v_Fy), GrowArrow(v_F))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()


class Scene13_Problem5_TwoCablesHook(Hibbeler3DScene):
    """Problem 5 (Slide 20 top): Two cables at hook A(0,0,4 ft) to B(3,-3,2.5) and C(2,4,0)."""

    def construct(self):
        axes, labels = self.setup_hibbeler_axes(
            x_range=(0, 5, 1), y_range=(-4, 5, 1), z_range=(-3, 5, 1)
        )
        self.add(axes, labels)

        A, B, C = (0, 0, 4), (3, -3, 2.5), (2, 4, 0)
        cable_AB = DashedLine(axes.c2p(*A), axes.c2p(*B), color=GRAY)
        cable_AC = DashedLine(axes.c2p(*A), axes.c2p(*C), color=GRAY)

        v_FB = self.arrow3d(axes, A, (2.0, -2.0, 3.0), color=BLUE)
        v_FC = self.arrow3d(axes, A, (1.25, 2.5, 1.5), color=GREEN)
        v_FR = self.arrow3d(axes, A, (3.25, 0.5, 0.5), color=RED, stroke_width=6)

        self.add_hud(
            [
                r"\text{Prob 5: } F_B = 600\text{ lb}, \; F_C = 750\text{ lb}",
                r"\mathbf{F}_B = \{400\mathbf{i} - 400\mathbf{j} - 200\mathbf{k}\}\text{ lb}",
                r"\mathbf{F}_C = \{250\mathbf{i} + 500\mathbf{j} - 500\mathbf{k}\}\text{ lb}",
                r"\mathbf{F}_R = \{650\mathbf{i} + 100\mathbf{j} - 700\mathbf{k}\}\text{ lb}, \; F_R = 960.5\text{ lb}",
            ],
            corner=UL,
        )

        self.play(Create(cable_AB), Create(cable_AC), GrowArrow(v_FB), GrowArrow(v_FC))
        self.play(GrowArrow(v_FR))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()


class Scene14_Problem6_TwoCablesRing(Hibbeler3DScene):
    """Problem 6 (Slide 20 bottom): Ring A(0,-2,4 m) with cables to B(0,0,0) and C(4,6,0)."""

    def construct(self):
        axes, labels = self.setup_hibbeler_axes(
            x_range=(0, 5, 1), y_range=(-3, 7, 2), z_range=(0, 5, 1)
        )
        self.add(axes, labels)

        A, B, C = (0, -2, 4), (0, 0, 0), (4, 6, 0)
        cable_AB = DashedLine(axes.c2p(*A), axes.c2p(*B), color=GRAY)
        cable_AC = DashedLine(axes.c2p(*A), axes.c2p(*C), color=GRAY)

        v_FAB = self.arrow3d(axes, A, (0, -0.6, 1.2), color=BLUE)
        v_FAC = self.arrow3d(axes, A, (1.5, 1.0, 2.5), color=GREEN)
        v_FR = self.arrow3d(axes, A, (1.5, 2.4, 0.3), color=RED, stroke_width=6)

        self.add_hud(
            [
                r"\text{Prob 6: } A(0, -2, 4)\text{ m}, \; B(0, 0, 0)\text{ m}, \; C(4, 6, 0)\text{ m}",
                r"\mathbf{F}_{AB} = \{268.3\mathbf{j} - 536.7\mathbf{k}\}\text{ N}",
                r"\mathbf{F}_{AC} = \{204.1\mathbf{i} + 408.2\mathbf{j} - 204.1\mathbf{k}\}\text{ N}",
                r"F_R = 1024\text{ N}, \; \alpha = 78.5^\circ, \; \beta = 48.6^\circ, \; \gamma = 136.3^\circ",
            ],
            corner=UL,
        )

        self.play(Create(cable_AB), Create(cable_AC), GrowArrow(v_FAB), GrowArrow(v_FAC))
        self.play(GrowArrow(v_FR))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()


class Scene15_Problem7_RifleVelocity(Hibbeler3DScene):
    """Problem 7 (Slide 21 top): Rifle fired from A to B with v = 1800 m/s."""

    def construct(self):
        axes, labels = self.setup_hibbeler_axes(
            x_range=(0, 5, 1), y_range=(0, 6, 1), z_range=(0, 4, 1)
        )
        self.add(axes, labels)

        A, B = (0, 0, 1.6), (3.2, 4.2, 0)
        box = self.create_parallelepiped(axes, (0, 0, 0), (3.2, 4.2, 1.6), color=BLUE_B)
        traj = DashedLine(axes.c2p(*A), axes.c2p(*B), color=YELLOW)
        vec_v = self.arrow3d(axes, A, B, color=RED, stroke_width=6)

        self.add_hud(
            [
                r"\text{Prob 7: Rifle Velocity } v = 1800\text{ m/s}",
                r"\mathbf{r}_{AB} = 160\mathbf{i} + 210\mathbf{j} - 80\mathbf{k}\text{ m}, \; |\mathbf{r}_{AB}| = 275.86\text{ m}",
                r"\mathbf{v} = 1800\frac{\mathbf{r}_{AB}}{|\mathbf{r}_{AB}|} = \{1044\mathbf{i} + 1370\mathbf{j} - 522\mathbf{k}\}\text{ m/s}",
            ],
            corner=UL,
        )

        self.play(Create(box), Create(traj))
        self.play(GrowArrow(vec_v))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()


class Scene16_Problem8_SliderRod(Hibbeler3DScene):
    """Problem 8 (Slide 21 bottom): Slider along guide rod from A(10,-8,0) to B(0,16,12)."""

    def construct(self):
        axes, labels = self.setup_hibbeler_axes(
            x_range=(0, 4, 1), y_range=(-3, 5, 1), z_range=(0, 4, 1)
        )
        self.add(axes, labels)

        A, B = (2.5, -2.0, 0), (0, 4.0, 3.0)
        rod = Line(axes.c2p(*A), axes.c2p(*B), color=GRAY_B, stroke_width=6)
        slider = Dot(axes.c2p(*A), radius=0.12, color=YELLOW)
        self.add_fixed_orientation_mobjects(slider)
        vec_v = self.arrow3d(axes, (1.25, 1.0, 1.5), (0.4, 3.0, 2.5), color=RED, stroke_width=6)

        self.add_hud(
            [
                r"\text{Prob 8: } A(10, -8, 0)\text{ m}, \; B(0, 16, 12)\text{ m}, \; v = 6\text{ m/s}",
                r"\mathbf{r}_{AB} = -10\mathbf{i} + 24\mathbf{j} + 12\mathbf{k}\text{ m}, \; |\mathbf{r}_{AB}| = 28.64\text{ m}",
                r"\text{(a) }\mathbf{u}_{AB} = -0.349\mathbf{i} + 0.838\mathbf{j} + 0.419\mathbf{k}",
                r"\text{(b) }\mathbf{v} = \{-2.10\mathbf{i} + 5.03\mathbf{j} + 2.51\mathbf{k}\}\text{ m/s}",
            ],
            corner=UL,
        )

        self.play(Create(rod), FadeIn(slider))
        self.play(slider.animate.move_to(axes.c2p(1.25, 1.0, 1.5)), GrowArrow(vec_v), run_time=2)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(2.5)
        self.stop_ambient_camera_rotation()


class Scene17_Problem9_PostCables(Hibbeler3DScene):
    """Problem 9 (Slide 22 top): Post C(0,0,4 ft) with cables to A and B(4,-7,0)."""

    def construct(self):
        axes, labels = self.setup_hibbeler_axes(
            x_range=(-3, 5, 1), y_range=(-8, 4, 2), z_range=(0, 5, 1)
        )
        self.add(axes, labels)

        C = (0, 0, 4)
        A = (-1.928, 2.298, 0)
        B = (4, -7, 0)

        post = Line(axes.c2p(0, 0, 0), axes.c2p(*C), color=BLUE_D, stroke_width=8)
        v_F1 = self.arrow3d(axes, C, A, color=GREEN)
        v_F2 = self.arrow3d(axes, C, B, color=BLUE)
        v_FR = self.arrow3d(axes, C, (-0.1, -0.8, 0.2), color=RED, stroke_width=6)

        self.add_hud(
            [
                r"\text{Prob 9: Post } C(0, 0, 4)\text{ ft}, \; F_1 = 100\text{ lb}, \; F_2 = 81\text{ lb}",
                r"\mathbf{F}_1 = \{-38.6\mathbf{i} + 46.0\mathbf{j} - 80.0\mathbf{k}\}\text{ lb}",
                r"\mathbf{F}_2 = \{36.0\mathbf{i} - 63.0\mathbf{j} - 36.0\mathbf{k}\}\text{ lb}",
                r"F_R = 117.3\text{ lb}, \; \alpha = 91.3^\circ, \; \beta = 98.4^\circ, \; \gamma = 171.6^\circ",
            ],
            corner=UL,
        )

        self.play(Create(post), GrowArrow(v_F1), GrowArrow(v_F2))
        self.play(GrowArrow(v_FR))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()


class Scene18_Problem10_TowerThreeCables(Hibbeler3DScene):
    """Problem 10 (Slide 22 bottom): Tower OD (24 m) held by three cables DA, DB, DC."""

    def construct(self):
        axes, labels = self.setup_hibbeler_axes(
            x_range=(-2, 5, 1), y_range=(-4, 4, 1), z_range=(0, 6, 1)
        )
        self.add(axes, labels)

        D = (0, 0, 4.8)
        A = (4.0, 3.0, 0)
        B = (-1.2, 0.8, 0)
        C = (3.2, -3.6, 0)

        tower = Line(axes.c2p(0, 0, 0), axes.c2p(*D), color=GRAY_A, stroke_width=8)
        c_DA = self.arrow3d(axes, D, A, color=BLUE)
        c_DB = self.arrow3d(axes, D, B, color=GREEN)
        c_DC = self.arrow3d(axes, D, C, color=YELLOW)
        v_FR = self.arrow3d(axes, D, (0.8, -0.05, 0.5), color=RED, stroke_width=6.5)

        self.add_hud(
            [
                r"\text{Prob 10: Tower } D(0,0,24)\text{ m}, \; A(20,15,0), \; B(-6,4,0), \; C(16,-18,0)",
                r"F_{DA} = 400\text{ N}, \quad F_{DB} = 800\text{ N}, \quad F_{DC} = 600\text{ N}",
                r"\mathbf{F}_R = \{321.7\mathbf{i} - 16.8\mathbf{j} - 1466.7\mathbf{k}\}\text{ N}",
                r"F_R = 1.50\text{ kN}, \; \alpha = 77.6^\circ, \; \beta = 90.6^\circ, \; \gamma = 167.6^\circ",
            ],
            corner=UL,
        )

        self.play(Create(tower), GrowArrow(c_DA), GrowArrow(c_DB), GrowArrow(c_DC))
        self.play(GrowArrow(v_FR))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()