#!/usr/bin/env bash
set -e

# Create output directories if they don't exist
mkdir -p assets/videos

# List of all 18 Manim scenes
SCENES=(
  "Scene01_2Dvs3DRightHandRule"
  "Scene02_CartesianParallelepiped"
  "Scene03_DirectionCosinesAndUnitVector"
  "Scene04_PositionVectors"
  "Scene05_Example1_EyeboltCable"
  "Scene06_Example2_DirectionAngles"
  "Scene07_Example3_DoubleProjection"
  "Scene08_Example4_ObtuseAngles"
  "Scene09_Problem1_ForceP"
  "Scene10_Problem2_BracketForce"
  "Scene11_Problem3_ResultantAlongX"
  "Scene12_Problem4_PoleForce"
  "Scene13_Problem5_TwoCablesHook"
  "Scene14_Problem6_TwoCablesRing"
  "Scene15_Problem7_RifleVelocity"
  "Scene16_Problem8_SliderRod"
  "Scene17_Problem9_PostCables"
  "Scene18_Problem10_TowerThreeCables"
)

echo "=================================================="
echo "Starting batch render of all 18 scenes at 1080p60..."
echo "=================================================="

for SCENE in "${SCENES[@]}"; do
  echo ">>> Rendering: $SCENE"
  # -qh specifies high quality (1080p60)
  manim -qh manim/mechanics_manim_scenes.py "$SCENE"
  
  # Copy finished video to your Quarto assets directory
  cp "media/videos/mechanics_manim_scenes/1080p60/${SCENE}.mp4" "assets/videos/${SCENE}.mp4"
  echo ">>> Completed and copied: ${SCENE}.mp4"
  echo "--------------------------------------------------"
done

echo "All 18 animations have been successfully rendered and saved to assets/videos/!"