#!/usr/bin/env python3
"""
Example usage for stereo matching with Middlebury dataset
(aka final script)
"""

from os import path
import cv2
import os
from stereomatch_all import process_stereo_pair, process_middlebury_dataset

def example_single_scene():
    """Example: Process a single scene"""
    
    # Get dataset path from environment variable or use default
    dataset_path = os.getenv('MIDDLEBURY_DATASET_PATH', "/path/to/your/middlebury/dataset")
    scene_name = "chess2"  # or "chess1", "curule1", etc.
    
    # Constructing l/r imagepaths
    left_path = path.join(dataset_path, scene_name, "im0.png")
    right_path = path.join(dataset_path, scene_name, "im1.png")
    
    # files exist?
    if not path.exists(left_path):
        print(f"Left image not found: {left_path}")
        return
    if not path.exists(right_path):
        print(f"Right image not found: {right_path}")
        return
    
    # Processing
    disparity = process_stereo_pair(left_path, right_path, "results")
    
    if disparity is not None:
        print("Successfully computed disparity map!")
        
        # Display the result (optional)
        cv2.imshow('Disparity Map', disparity)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def example_multiple_scenes():
    """Example: Process all scenes in the dataset"""
    
    # Get dataset path from environment variable or use default
    dataset_path = os.getenv('MIDDLEBURY_DATASET_PATH', "/path/to/your/middlebury/dataset")
    
    if path.exists(dataset_path):
        process_middlebury_dataset(dataset_path, "results")
    else:
        print(f"Dataset path does not exist: {dataset_path}")

def example_with_relative_paths():
    """Example: If you want to copy some images to your current directory"""
    
    # You could copy specific images to your current directory
    # and then use relative paths
    
    left_path = "left.png"  # Image in current directory
    right_path = "right.png"  # Image in current directory
    
    if path.exists(left_path) and path.exists(right_path):
        disparity = process_stereo_pair(left_path, right_path, "results")
        print("Processed images from current directory")
    else:
        print("Images not found in current directory")

if __name__ == "__main__":
    print("Stereo Matching Examples")
    print("========================")
    
    # Uncomment the example you want to run:
    
    # Example 1: Process a single scene
    example_single_scene()
    
    # Example 2: Process all scenes
    # example_multiple_scenes()
    
    # Example 3: Use images in current directory
    #example_with_relative_paths()
    
    print("\nTo use these examples:")
    print("1. Update the dataset_path variable with your actual Middlebury dataset path")
    print("2. Uncomment the example you want to run")
    print("3. Run the script: python example_usage.py")
    
    print("\nCommon Middlebury dataset structure:")
    print("dataset_root/")
    print("├── cones/")
    print("│   ├── im2.png  (left image)")
    print("│   ├── im6.png  (right image)")
    print("│   └── ...")
    print("├── teddy/")
    print("│   ├── im2.png")
    print("│   ├── im6.png")
    print("│   └── ...")
    print("└── ...") 