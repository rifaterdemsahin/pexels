# Stock Videos and Photos Output

This directory contains the downloaded stock videos and photos from Pexels API based on the input configuration files.

## Directory Structure

```
output/
├── StockVideos/         # Downloaded video assets
│   ├── V_01.mp4         # Video file
│   ├── V_01_meta.json   # Video metadata
│   ├── V_02.mp4
│   ├── V_02_meta.json
│   └── ...
└── StockImages/         # Downloaded image assets
    ├── icon_github.jpg
    ├── icon_github_meta.json
    ├── test_image_001.jpg
    ├── test_image_001_meta.json
    └── ...
```

## Asset Types

### Videos
- Sourced from `input/batch_generation_data.yaml`
- Fetched using `search_query` field from each video configuration
- Saved as MP4 files with corresponding metadata

### Images
- Sourced from `input/assets_config.json` and `input/icons.json`
- Fetched using keywords derived from the `prompt` field
- Saved as JPG files with corresponding metadata

## Metadata Files

Each asset has an accompanying `*_meta.json` file containing:
- Original configuration (ID, name, priority, prompt/query)
- Pexels API response data (photographer, dimensions, URLs, etc.)
- Source information for attribution

## Processing Script

Assets are generated using:
```bash
cd /home/runner/work/pexels/pexels/3_Simulation/2025-02-14
python3 process_assets.py
```

Requires:
- PEXELS_API_KEY environment variable or .env file
- Python 3 with requests, python-dotenv, and PyYAML

## Attribution

All assets are sourced from [Pexels](https://www.pexels.com/) which provides free stock photos and videos. Please ensure proper attribution as per Pexels license when using these assets.
