# Pexels Stock Footage Generator

Stock footage generation for videos over API using Python and the Pexels API.

## Features

- Search for stock videos by keyword
- Get popular/curated videos
- Retrieve specific videos by ID
- Download video information and file URLs
- Support for filtering by orientation and size
- Secure API key management using environment variables

## Prerequisites

- Python 3.7 or higher
- Pexels API key (free at https://www.pexels.com/api/)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/rifaterdemsahin/pexels.git
cd pexels
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key:

   **Option A: Using .env file (recommended for local development)**
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```

   **Option B: Using environment variable**
   ```bash
   export PEXELS_API_KEY=your_api_key_here
   ```

## Usage

### Basic Usage

Run the script to search for videos:

```bash
python pexels_video_fetcher.py
```

### Using as a Module

```python
from pexels_video_fetcher import PexelsVideoFetcher

# Initialize the fetcher
fetcher = PexelsVideoFetcher()

# Search for videos
results = fetcher.search_videos("nature", per_page=10)

# Display video information
if results and results.get('videos'):
    for video in results['videos']:
        fetcher.display_video_info(video)

# Get popular videos
popular = fetcher.get_popular_videos(per_page=5)

# Get specific video by ID
video = fetcher.get_video_by_id(12345)
```

### Advanced Search Options

```python
# Search with filters
results = fetcher.search_videos(
    query="ocean",
    per_page=20,
    page=1,
    orientation="landscape",  # 'landscape', 'portrait', or 'square'
    size="large"              # 'large', 'medium', or 'small'
)
```

## API Key Management

### Local Development
- Store your API key in a `.env` file (automatically git-ignored)
- The `.env` file is excluded from version control for security

### GitHub Actions / CI/CD
- Add `PEXELS_API_KEY` as a GitHub Secret
- See [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) for detailed instructions

### Security Notes
- ✅ `.env` file is git-ignored
- ✅ Use GitHub Secrets for CI/CD
- ❌ Never commit API keys to the repository
- ❌ Never share your API key publicly

## Project Structure

```
pexels/
├── .env.example           # Template for environment variables
├── .gitignore            # Git ignore file (excludes .env)
├── requirements.txt      # Python dependencies
├── pexels_video_fetcher.py  # Main Python script
├── GITHUB_ACTIONS_SETUP.md  # GitHub Actions configuration guide
└── README.md            # This file
```

## API Documentation

For more information about the Pexels API, visit:
- API Documentation: https://www.pexels.com/api/documentation/
- Get API Key: https://www.pexels.com/api/

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
