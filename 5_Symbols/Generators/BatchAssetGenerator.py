#!/usr/bin/env python3
"""
Batch Asset Generator
Reads batch_generation_data.yaml and fetches video and image assets from Pexels.
"""

import os
import sys
import yaml
import json
import argparse
import requests
from pathlib import Path

# Add Utils directory to path to import helpers
# Assumes structure: 
# 5_Symbols/
#   Generators/BatchAssetGenerator.py
#   Utils/pexels_video_fetcher.py
utils_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Utils'))
if utils_path not in sys.path:
    sys.path.append(utils_path)

try:
    from pexels_video_fetcher import PexelsVideoFetcher
except ImportError:
    print(f"Error: Could not import PexelsVideoFetcher from {utils_path}")
    print("Ensure 5_Symbols/Utils/pexels_video_fetcher.py exists.")
    sys.exit(1)

def load_config(config_path):
    """Load the YAML configuration file."""
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        return None
    
    with open(config_path, 'r') as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
            return None

def download_file(url, filepath):
    """Downloads a file from a URL to the specified filepath."""
    if os.path.exists(filepath):
        print(f"    File already exists at {filepath}")
        return True

    print(f"    Downloading to {filepath}...")
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("    Download complete.")
        return True
    except Exception as e:
        print(f"    Error downloading: {e}")
        return False

def process_section(section, fetcher, videos_base_dir, images_base_dir):
    """Process a single section."""
    section_id = section.get('id')
    title = section.get('title')
    print(f"\nProcessing section: {section_id} - {title}")
    
    # Create output directories for this section
    section_videos_dir = os.path.join(videos_base_dir, section_id)
    section_images_dir = os.path.join(images_base_dir, section_id)
    
    os.makedirs(section_videos_dir, exist_ok=True)
    os.makedirs(section_images_dir, exist_ok=True)
    
    # Process Videos
    video_keywords = section.get('video_keywords', [])
    for keyword in video_keywords[:3]: # Limit to first 3 keywords
        print(f"  Searching videos for: {keyword}")
        results = fetcher.search_videos(keyword, per_page=1, orientation='landscape', size='medium')
        
        if results and results.get('videos'):
            for video in results['videos']:
                # fetcher.display_video_info(video) # Optional: reduce verbosity
                
                # Download video
                video_files = video.get('video_files', [])
                if video_files:
                    # Sort by width to get best quality (descending)
                    video_files.sort(key=lambda x: x.get('width', 0), reverse=True)
                    best_video = video_files[0]
                    download_url = best_video.get('link')
                    
                    if download_url:
                        filename = f"{section_id}_{video['id']}.mp4"
                        filepath = os.path.join(section_videos_dir, filename)
                        download_file(download_url, filepath)
                            
                # Save metadata
                meta_file = os.path.join(section_videos_dir, f"{section_id}_{video['id']}_meta.json")
                with open(meta_file, 'w') as f:
                    json.dump(video, f, indent=2)
        else:
            print(f"  No videos found for {keyword}")

    # Process Images
    image_keywords = section.get('image_keywords', [])
    for keyword in image_keywords[:3]: # Limit to first 3 keywords
        print(f"  Searching images for: {keyword}")
        results = fetcher.search_photos(keyword, per_page=1, orientation='landscape', size='medium')
        
        if results and results.get('photos'):
            for photo in results['photos']:
                # fetcher.display_photo_info(photo)
                
                # Download photo
                download_url = photo.get('src', {}).get('original')
                if download_url:
                    filename = f"{section_id}_{photo['id']}.jpg"
                    filepath = os.path.join(section_images_dir, filename)
                    download_file(download_url, filepath)

                # Save metadata
                meta_file = os.path.join(section_images_dir, f"{section_id}_{photo['id']}_meta.json")
                with open(meta_file, 'w') as f:
                    json.dump(photo, f, indent=2)
        else:
            print(f"  No images found for {keyword}")

def main():
    parser = argparse.ArgumentParser(description="Batch Asset Generator")
    parser.add_argument("--config", required=True, help="Path to batch_generation_data.yaml")
    parser.add_argument("--output-dir", required=True, help="Base directory for output (e.g. 3_Simulation/WeekX)")
    args = parser.parse_args()

    config_path = args.config
    output_dir = args.output_dir
    
    videos_base_dir = os.path.join(output_dir, 'StockVideos')
    images_base_dir = os.path.join(output_dir, 'StockImages')
    
    # Load config
    print(f"Loading config from {config_path}...")
    config = load_config(config_path)
    if not config:
        sys.exit(1)
        
    sections = config.get('sections', [])
    if not sections:
        print("No sections found in config.")
        sys.exit(1)
        
    # Initialize Pexels Fetcher
    try:
        fetcher = PexelsVideoFetcher()
    except ValueError as e:
        print(f"Error initializing fetcher: {e}")
        print("Please set PEXELS_API_KEY environment variable.")
        sys.exit(1)
        
    print(f"Found {len(sections)} sections to process.")
    print(f"Outputting to: {output_dir}")
    
    for section in sections:
        process_section(section, fetcher, videos_base_dir, images_base_dir)
                
    print("\nBatch processing completed.")

if __name__ == "__main__":
    main()

import os
import sys
import yaml
import json
from pathlib import Path

# Add current directory to path to import pexels_video_fetcher
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pexels_video_fetcher import PexelsVideoFetcher

def load_config(config_path):
    """Load the YAML configuration file."""
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        return None
    
    with open(config_path, 'r') as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
            return None

def main():
    # Define paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    config_path = os.path.join(base_dir, '3_Simulation', 'Feb1', '_source', 'batch_generation_data.yaml')
    # User requested specific download folders
    videos_base_dir = os.path.join(base_dir, '3_Simulation', 'Feb1', 'StockVideos')
    images_base_dir = os.path.join(base_dir, '3_Simulation', 'Feb1', 'StockImages')
    
    # Load config
    print(f"Loading config from {config_path}...")
    config = load_config(config_path)
    if not config:
        sys.exit(1)
        
    sections = config.get('sections', [])
    if not sections:
        print("No sections found in config.")
        sys.exit(1)
        
    # Initialize Pexels Fetcher
    try:
        fetcher = PexelsVideoFetcher()
    except ValueError as e:
        print(f"Error initializing fetcher: {e}")
        print("Please set PEXELS_API_KEY environment variable.")
        sys.exit(1)
        
    print(f"Found {len(sections)} sections to process.")
    
    for section in sections:
        section_id = section.get('id')
        title = section.get('title')
        print(f"\nProcessing section: {section_id} - {title}")
        
        # Create output directories for this section
        section_videos_dir = os.path.join(videos_base_dir, section_id)
        section_images_dir = os.path.join(images_base_dir, section_id)
        
        os.makedirs(section_videos_dir, exist_ok=True)
        os.makedirs(section_images_dir, exist_ok=True)
        
        # Process Videos
        video_keywords = section.get('video_keywords', [])
        for keyword in video_keywords[:3]: # Limit to first 3 keywords
            print(f"  Searching videos for: {keyword}")
            results = fetcher.search_videos(keyword, per_page=1, orientation='landscape', size='medium')
            
            if results and results.get('videos'):
                for video in results['videos']:
                    fetcher.display_video_info(video)
                    
                    # Download video
                    video_files = video.get('video_files', [])
                    if video_files:
                        # Sort by width to get best quality (descending)
                        video_files.sort(key=lambda x: x.get('width', 0), reverse=True)
                        best_video = video_files[0]
                        download_url = best_video.get('link')
                        
                        if download_url:
                            # Prefix filename with section_id
                            filename = f"{section_id}_{video['id']}.mp4"
                            filepath = os.path.join(section_videos_dir, filename)
                            
                            # Download if not exists
                            if not os.path.exists(filepath):
                                print(f"    Downloading video to {filepath}...")
                                try:
                                    import requests
                                    with requests.get(download_url, stream=True) as r:
                                        r.raise_for_status()
                                        with open(filepath, 'wb') as f:
                                            for chunk in r.iter_content(chunk_size=8192):
                                                f.write(chunk)
                                    print("    Download complete.")
                                except Exception as e:
                                    print(f"    Error downloading video: {e}")
                            else:
                                print(f"    Video already exists at {filepath}")
                                
                    # Save metadata
                    meta_file = os.path.join(section_videos_dir, f"{section_id}_{video['id']}_meta.json")
                    with open(meta_file, 'w') as f:
                        json.dump(video, f, indent=2)
            else:
                print(f"  No videos found for {keyword}")

        # Process Images
        image_keywords = section.get('image_keywords', [])
        for keyword in image_keywords[:3]: # Limit to first 3 keywords
            print(f"  Searching images for: {keyword}")
            results = fetcher.search_photos(keyword, per_page=1, orientation='landscape', size='medium')
            
            if results and results.get('photos'):
                for photo in results['photos']:
                    fetcher.display_photo_info(photo)
                    
                    # Download photo
                    download_url = photo.get('src', {}).get('original')
                    if download_url:
                        # Prefix filename with section_id
                        filename = f"{section_id}_{photo['id']}.jpg"
                        filepath = os.path.join(section_images_dir, filename)
                        
                        # Download if not exists
                        if not os.path.exists(filepath):
                            print(f"    Downloading photo to {filepath}...")
                            try:
                                import requests
                                with requests.get(download_url, stream=True) as r:
                                    r.raise_for_status()
                                    with open(filepath, 'wb') as f:
                                        for chunk in r.iter_content(chunk_size=8192):
                                            f.write(chunk)
                                print("    Download complete.")
                            except Exception as e:
                                print(f"    Error downloading photo: {e}")
                        else:
                            print(f"    Photo already exists at {filepath}")

                    # Save metadata
                    meta_file = os.path.join(section_images_dir, f"{section_id}_{photo['id']}_meta.json")
                    with open(meta_file, 'w') as f:
                        json.dump(photo, f, indent=2)
            else:
                print(f"  No images found for {keyword}")
                
    print("\nBatch processing completed.")

if __name__ == "__main__":
    main()
