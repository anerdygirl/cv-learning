# helper script for stereo matching
# can be executed as a script (process the entire dataset) or imported as a module

import cv2
import numpy as np
from os import path, makedirs, listdir
import glob
import os


def process_stereo_pair(left_path, right_path, output_dir=None):
    """
    Process a stereo pair and compute disparity map using SGBM
    
    Args:
        left_path: Path to left image
        right_path: Path to right image
        output_dir: Directory to save results (optional)
    """
    
    # Load images
    imgL = cv2.imread(left_path, 0)  # Grayscale
    imgR = cv2.imread(right_path, 0)  # Grayscale
    
    if imgL is None or imgR is None:
        print(f"Error: Could not load images")
        print(f"Left path: {left_path}")
        print(f"Right path: {right_path}")
        return None
    
    print(f"Processing: {path.basename(left_path)} and {path.basename(right_path)}")
    print(f"Image shapes: Left {imgL.shape}, Right {imgR.shape}")
    
    # Create SGBM object with better parameters for Middlebury dataset
    window_size = 5
    min_disp = 0
    num_disp = 160 # must be divisible by 16
    
    sgbm = cv2.StereoSGBM_create(
        minDisparity=min_disp,
        numDisparities=num_disp,
        blockSize=window_size,
        P1=8 * 3 * window_size**2,
        P2=32 * 3 * window_size**2,
        disp12MaxDiff=1,
        uniquenessRatio=10,
        speckleWindowSize=100,
        speckleRange=32
    )
    
    # Compute disparity
    disparity = sgbm.compute(imgL, imgR)
    
    # Normalize disparity for visualization
    disparity_normalized = cv2.normalize(disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    
    # Save results if output directory is specified
    if output_dir:
        makedirs(output_dir, exist_ok=True)
        scene_name = path.basename(path.dirname(left_path))
        
        # Save disparity map
        disparity_path = path.join(output_dir, f"{scene_name}_disparity.png")
        cv2.imwrite(disparity_path, disparity_normalized)
        print(f"Saved disparity map to: {disparity_path}")
        
        # Save original images for reference
        cv2.imwrite(path.join(output_dir, f"{scene_name}_left.png"), imgL)
        cv2.imwrite(path.join(output_dir, f"{scene_name}_right.png"), imgR)
    
    return disparity_normalized

def process_middlebury_dataset(dataset_path, output_dir="results"):
    """
    Process all scenes in a Middlebury dataset
    
    Args:
        dataset_path: Path to the Middlebury dataset root directory
        output_dir: Directory to save results
    """
    
    # Common Middlebury image naming patterns
    left_patterns = ["im0.png", "im2.png", "left.png", "view1.png"]
    right_patterns = ["im1.png", "im6.png", "right.png", "view5.png"]
    
    # Find all scene directories
    scene_dirs = [d for d in listdir(dataset_path) 
                  if path.isdir(path.join(dataset_path, d))]
    
    print(f"Found {len(scene_dirs)} scenes: {scene_dirs}")
    
    for scene in scene_dirs:
        scene_path = path.join(dataset_path, scene)
        print(f"\nProcessing scene: {scene}")
        
        # Try to find left and right images
        left_found = False
        right_found = False
        
        for left_pattern in left_patterns:
            left_path = path.join(scene_path, left_pattern)
            if path.exists(left_path):
                left_found = True
                break
        
        for right_pattern in right_patterns:
            right_path = path.join(scene_path, right_pattern)
            if path.exists(right_path):
                right_found = True
                break
        
        if left_found and right_found:
            disparity = process_stereo_pair(left_path, right_path, output_dir)
            if disparity is not None:
                print(f"Successfully processed {scene}")
        else:
            print(f"Could not find stereo pair for {scene}")
            print(f"Available files in {scene}: {listdir(scene_path)}")

# Example usage
if __name__ == "__main__":
    # Get dataset path from environment variable or use default
    dataset_path = os.getenv('MIDDLEBURY_DATASET_PATH', "/path/to/your/middlebury/dataset")
    
    if path.exists(dataset_path):
        process_middlebury_dataset(dataset_path)
    else:
        print(f"Dataset path does not exist: {dataset_path}")
        print("Please update the dataset_path variable with your actual path")