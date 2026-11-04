import subprocess
import os

scenes = [
    "Scene01_2Dvs3DRightHandRule",
    "Scene02_CartesianParallelepiped",
    "Scene03_DirectionCosinesAndUnitVector",
    "Scene04_PositionVectors",
    "Scene05_Example1_EyeboltCable",
    "Scene06_Example2_DirectionAngles",
    "Scene07_Example3_DoubleProjection",
    "Scene08_Example4_ObtuseAngles",
    "Scene09_Problem1_ForceP",
    "Scene10_Problem2_BracketForce",
    "Scene11_Problem3_ResultantAlongX",
    "Scene12_Problem4_PoleForce",
    "Scene13_Problem5_TwoCablesHook",
    "Scene14_Problem6_TwoCablesRing",
    "Scene15_Problem7_RifleVelocity",
    "Scene16_Problem8_SliderRod",
    "Scene17_Problem9_PostCables",
    "Scene18_Problem10_TowerThreeCables"
]

os.makedirs("assets/videos", exist_ok=True)

print("==================================================")
print("Starting batch render of all 18 scenes at 1080p60...")
print("==================================================")

for scene in scenes:
    print(f"\n>>> Rendering: {scene}")
    # -qh runs high quality 1080p60
    subprocess.run(["manim", "-qh", "manim/mechanics_manim_scenes.py", scene], check=True)
    
    src = f"media/videos/mechanics_manim_scenes/1080p60/{scene}.mp4"
    dst = f"assets/videos/{scene}.mp4"
    
    if os.path.exists(src):
        os.replace(src, dst)
        print(f">>> Completed and copied to: {dst}")
    else:
        print(f">>> Warning: Expected output not found for {scene}")

print("\nAll 18 animations have been successfully rendered and saved to assets/videos/!")