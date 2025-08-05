# disparity map from stereo images using SGBM algorithm and middlebury dataset
"""
Pretty much same as stereomatch_single_scene.py except you have to manually set the scene here
"""

import cv2
import numpy as np
from os import path, makedirs

# Define the path to your Middlebury dataset
dataset_path = "/your/Middleblurry/dataset/path"
scene_name = "artroom1"  # Change this to your scene name (e.g., "artroom1", "chess1", "curule1", etc.)

# Construct paths to left and right images
left_image_path = path.join(dataset_path, scene_name, "im0.png")  # left image
right_image_path = path.join(dataset_path, scene_name, "im1.png")  # right image

# load stereo images
imgL = cv2.imread(left_image_path, 0)  # 0 means grayscale
imgR = cv2.imread(right_image_path, 0)  # 0 means grayscale

# Check if images were loaded successfully
if imgL is None:
    print(f"Error: Could not load left image from {left_image_path}")
    exit()
if imgR is None:
    print(f"Error: Could not load right image from {right_image_path}")
    exit()

print(f"Left image shape: {imgL.shape}")
print(f"Right image shape: {imgR.shape}")

# Create SGBM object with better parameters for Middlebury dataset
window_size = 5
min_disp = 0
num_disp = 160  # Must be divisible by 16

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
print("Computing disparity map...")
disparity = sgbm.compute(imgL, imgR)

# Normalize disparity for visualization
disparity_normalized = cv2.normalize(disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

# Create output directory
output_dir = "results"
makedirs(output_dir, exist_ok=True)

# Save results
disparity_path = path.join(output_dir, f"{scene_name}_disparity.png")
cv2.imwrite(disparity_path, disparity_normalized)
print(f"Saved disparity map to: {disparity_path}")

# Save original images for reference
cv2.imwrite(path.join(output_dir, f"{scene_name}_left.png"), imgL)
cv2.imwrite(path.join(output_dir, f"{scene_name}_right.png"), imgR)

# Display results (optional)
print("Displaying results...")
cv2.imshow('Left Image', imgL)
cv2.imshow('Right Image', imgR)
cv2.imshow('Disparity Map', disparity_normalized)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Processing complete!")
