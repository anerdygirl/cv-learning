#!/usr/bin/env python3
"""
Simple script to process a specific scene from the Middlebury dataset
Usage: python process_scene.py <scene_name>
Example: python process_scene.py artroom1
Same as stereosgbm.py except it's more command-line oritented
"""

import cv2
import numpy as np
from os import path, listdir
import sys
from stereomatch_all import process_stereo_pair

def main():
    if len(sys.argv) != 2:
        print("Usage: python process_scene.py <scene_name>")
        print("Available scenes:") # as of Middleblurry 2021 dataset.
        print("artroom1, artroom2, bandsaw1, bandsaw2, chess1, chess2, chess3, curule1, curule2, curule3, ladder1, ladder2")
        print("octogons1, octogons2", "pendulum1, pendulum2, podium1, skates1, skates2")
        print("skiboots1, skiboots2, skiboots3", "traproom1, traproom2")
        sys.exit(1)
    
    scene_name = sys.argv[1]
    # Get dataset path from environment variable or use local
    dataset_path = "your/Middleblurry/dataset/path"
    
    # Check if scene exists
    scene_path = path.join(dataset_path, scene_name)
    if not path.exists(scene_path):
        print(f"Scene '{scene_name}' not found in {dataset_path}")
        print("Available scenes:")
        scenes = [d for d in listdir(dataset_path) 
                  if path.isdir(path.join(dataset_path, d))]
        for scene in sorted(scenes):
            print(f"  {scene}")
        sys.exit(1)
    
    # Process the scene
    print(f"Processing scene: {scene_name}")
    left_path = path.join(scene_path, "im0.png")
    right_path = path.join(scene_path, "im1.png")
    
    disparity = process_stereo_pair(left_path, right_path, "results")
    
    if disparity is not None:
        print(f"Successfully processed {scene_name}!")
        print(f"Results saved in results/{scene_name}_disparity.png")
    else:
        print(f"Failed to process {scene_name}")

if __name__ == "__main__":
    main() 
