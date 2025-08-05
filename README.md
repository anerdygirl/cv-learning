# Stereo Matching with OpenCV SGBM

This repository contains Python scripts for computing disparity maps from stereo image pairs using OpenCV's SGBM (Semi-Global Block Matching) algorithm.

## Features

- Process single stereo pairs or entire datasets
- Optimized parameters for Middlebury dataset
- Multiple usage examples
- Flexible input/output handling

## Files

- `stereomatch_all.py` - Main module with stereo matching functions
- `stereomatch_single_scene.py` - Script to process a single scene
- `stereomatch_flexible.py` - Example usage with different scenarios
- `stereosgbm.py` - Basic stereo matching script
- `calculate_depth.py` - Additional depth calculation utilities

## Requirements

```bash
pip install opencv-python numpy
```

## Usage

### Setup

Set your dataset path as an environment variable:

```bash
export MIDDLEBURY_DATASET_PATH="/path/to/your/middlebury/dataset"
```

Or on Windows:
```cmd
set MIDDLEBURY_DATASET_PATH=C:\path\to\your\middlebury\dataset
```

### Process a Single Scene

```bash
python stereomatch_single_scene.py <scene_name>
```

Example:
```bash
python stereomatch_single_scene.py chess2
```

### Process All Scenes in Dataset

```python
from stereomatch_all import process_middlebury_dataset

# Update this path to your dataset location
dataset_path = "/path/to/your/middlebury/dataset"
process_middlebury_dataset(dataset_path, "results")
```

### Use as a Module

```python
from stereomatch_all import process_stereo_pair

left_path = "path/to/left/image.png"
right_path = "path/to/right/image.png"
disparity = process_stereo_pair(left_path, right_path, "output_dir")
```

## Dataset Structure

The scripts expect a Middlebury-style dataset structure:

```
dataset_root/
├── scene1/
│   ├── im0.png  (left image)
│   ├── im1.png  (right image)
│   └── ...
├── scene2/
│   ├── im0.png
│   ├── im1.png
│   └── ...
└── ...
```

## Output

- Disparity maps saved as PNG files
- Original left/right images for reference
- Results stored in `results/` directory by default

## Parameters

The SGBM algorithm uses the following optimized parameters:
- `numDisparities`: 160 (must be divisible by 16)
- `blockSize`: 5
- `P1`: 8 * 3 * window_size²
- `P2`: 32 * 3 * window_size²
- `uniquenessRatio`: 10
- `speckleWindowSize`: 100
- `speckleRange`: 32

## Notes

- Images are loaded in grayscale for optimal performance
- Disparity maps are normalized to 0-255 range for visualization
- The `results/` directory is excluded from version control by default

## License

[Add your license information here] 