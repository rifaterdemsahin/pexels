# 5_Symbols - Core Source Code

Contains the main application files and tools for the Pexels Stock Footage Automation.

## Directory Structure

* **Generators/**: Contains the main asset generation scripts.
  * `BatchAssetGenerator.py`: Main script to download video/images based on a YAML config.
* **Utils/**: Helper libraries and utility scripts.
  * `PexelsVideoFetcher.py`: Pexels API wrapper.
  * `FixAssetNaming.py`: Utility to ensure asset filenames are prefixed with their folder name.

## Usage

### Batch Asset Generator

Use this tool to generate assets for a specific week or project.

```bash
# Example for a specific week
python 5_Symbols/Generators/BatchAssetGenerator.py --config 3_Simulation/Feb1/_source/batch_generation_data.yaml --output-dir 3_Simulation/Feb1
```

### Fix Asset Naming

Run this if you manually added files and want to enforce the naming convention (Folder_Filename.ext).

```bash
python 5_Symbols/Utils/FixAssetNaming.py 3_Simulation/Feb1
```
