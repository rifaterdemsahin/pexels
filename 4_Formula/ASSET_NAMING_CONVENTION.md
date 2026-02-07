# Asset Naming Convention Formula

This document outlines the standard naming conventions for generated assets within the project.

## Objective

To ensure traceablity and organization of assets generated for video production, allowing for easy identification of which section of the video an asset belongs to.

## Convention Pattern

All downloaded assets (videos and images) must follow this pattern:

`{SectionID}_{AssetID}.{Extension}`

### Definitions

- **SectionID**: The unique identifier of the video section (e.g., `01_hook_problem`, `06_para_obsidian`). These correspond to the folder names derived from `batch_generation_data.yaml`.
- **AssetID**: The unique ID assigned by the asset provider (e.g., Pexels Video ID `8947696`).
- **Extension**: The file extension (e.g., `.jpg`, `.mp4`, `.json`).

## Examples

### Images

- **Original**: `8947696.jpg` located in `06_para_obsidian/`
- **Standardized**: `06_para_obsidian_8947696.jpg`

### Videos

- **Original**: `123456.mp4` located in `01_hook_problem/`
- **Standardized**: `01_hook_problem_123456.mp4`

### Metadata

- **Original**: `8947696_meta.json`
- **Standardized**: `06_para_obsidian_8947696_meta.json`

## Implementation

The `BatchAssetGenerator.py` script automatically applies this convention during download.
The `FixAssetNaming.py` script can be used to retroactively apply this convention to existing files.
