# 2025-02-14 Simulation: Stock Videos and Photos Processing

This simulation processes input configuration files to fetch and download stock videos and photos from the Pexels API.

## Overview

The processing script reads configuration files from the `input/` directory and fetches corresponding stock media assets from Pexels, saving them to the `output/` directory.

## Directory Structure

```
2025-02-14/
├── input/                              # Input configuration files
│   ├── batch_generation_data.yaml      # Video asset configurations
│   ├── assets_config.json              # Image asset configurations
│   ├── icons.json                      # Icon asset configurations
│   └── ... (other source files)
├── output/                             # Generated output
│   ├── StockVideos/                    # Downloaded videos
│   └── StockImages/                    # Downloaded images
├── process_assets.py                   # Main processing script
└── readme.md                           # This file
```

## Input Files

### 1. batch_generation_data.yaml
Contains video asset configurations with:
- `id`: Unique identifier for the video
- `name`: Descriptive name
- `search_query`: Pexels search query to find relevant videos
- `priority`: Asset priority (HIGH, MEDIUM, LOW)
- Additional metadata (scene, prompt, model info)

### 2. assets_config.json
Contains image asset configurations with:
- `id`: Unique identifier for the image
- `prompt`: Description used to generate search query
- Additional metadata

### 3. icons.json
Contains icon-specific image configurations, similar structure to assets_config.json

## Usage

### Prerequisites

1. **Python 3.7+** with required packages:
   ```bash
   pip install -r ../../requirements.txt
   ```

2. **Pexels API Key**: Get your free API key from [https://www.pexels.com/api/](https://www.pexels.com/api/)

3. **Set up environment variable**:
   ```bash
   export PEXELS_API_KEY="your_api_key_here"
   ```
   
   Or create a `.env` file in the repository root:
   ```
   PEXELS_API_KEY=your_api_key_here
   ```

### Running the Script

```bash
cd /home/runner/work/pexels/pexels/3_Simulation/2025-02-14
python3 process_assets.py
```

The script will:
1. Load all configuration files from `input/`
2. For each video entry, search Pexels and download the best quality match
3. For each image entry, search Pexels and download the original quality photo
4. Save all assets with metadata to `output/StockVideos/` and `output/StockImages/`

## Output

### Video Assets
- **Format**: MP4 files
- **Naming**: `{video_id}.mp4` (e.g., `V_01.mp4`)
- **Metadata**: `{video_id}_meta.json`

### Image Assets
- **Format**: JPG files
- **Naming**: `{image_id}.jpg` (e.g., `icon_github.jpg`)
- **Metadata**: `{image_id}_meta.json`

### Metadata Files
Each `*_meta.json` file contains:
- Configuration details (ID, name, search query/prompt)
- Pexels API response (photographer, dimensions, URLs)
- Attribution information

## Features

- **Automatic quality selection**: Downloads best available quality
- **Duplicate prevention**: Skips already downloaded files
- **Detailed logging**: Shows progress and any errors
- **Metadata preservation**: Saves full Pexels data for attribution
- **Error handling**: Continues processing if individual assets fail

## Attribution

All assets are sourced from [Pexels](https://www.pexels.com/), which provides free stock photos and videos. The license allows:
- ✅ Free for personal and commercial use
- ✅ No attribution required (but appreciated)
- ✅ Modification and editing allowed

Metadata files include photographer information for proper attribution if desired.

## Troubleshooting

### "Pexels API key is required"
- Ensure PEXELS_API_KEY is set in environment or .env file
- Verify the API key is valid

### "No videos/photos found"
- Check if the search query is too specific
- Try broader search terms
- Verify internet connection

### Import errors
- Run: `pip install -r ../../requirements.txt`
- Ensure you're using Python 3.7 or higher

## Related Files

- Main utilities: `/home/runner/work/pexels/pexels/5_Symbols/Utils/`
  - `pexels_video_fetcher.py`: Pexels API wrapper
  - `pexels_photo_fetcher.py`: Photo-specific methods
- Batch generator: `/home/runner/work/pexels/pexels/5_Symbols/Generators/BatchAssetGenerator.py`

## Notes

- The script respects Pexels API rate limits
- Downloaded files are cached (not re-downloaded if they exist)
- Processing time depends on number of assets and network speed
- Budget considerations mentioned in YAML files are for AI generation, not for Pexels API usage (which is free)

