#!/usr/bin/env python3
"""
Batch Asset Generator
Reads batch_generation_data.yaml and fetches video and image assets from Pexels.
"""

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
    output_base_dir = os.path.join(base_dir, '3_Simulation', 'Feb1', 'Assets')
    
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
        
        # Create output directories
        section_dir = os.path.join(output_base_dir, section_id)
        videos_dir = os.path.join(section_dir, 'videos')
        images_dir = os.path.join(section_dir, 'images')
        
        os.makedirs(videos_dir, exist_ok=True)
        os.makedirs(images_dir, exist_ok=True)
        
        # Process Videos
        video_keywords = section.get('video_keywords', [])
        for keyword in video_keywords[:3]: # Limit to first 3 keywords
            print(f"  Searching videos for: {keyword}")
            results = fetcher.search_videos(keyword, per_page=2, orientation='landscape', size='medium')
            
            if results and results.get('videos'):
                for video in results['videos']:
                    fetcher.display_video_info(video)
                    # In a real batch downloader, we would download the file here.
                    # For now, we save the metadata.
                    meta_file = os.path.join(videos_dir, f"{video['id']}_meta.json")
                    with open(meta_file, 'w') as f:
                        json.dump(video, f, indent=2)
            else:
                print(f"  No videos found for {keyword}")

        # Process Images
        image_keywords = section.get('image_keywords', [])
        for keyword in image_keywords[:3]: # Limit to first 3 keywords
            print(f"  Searching images for: {keyword}")
            results = fetcher.search_photos(keyword, per_page=2, orientation='landscape', size='medium')
            
            if results and results.get('photos'):
                for photo in results['photos']:
                    fetcher.display_photo_info(photo)
                    # Similarly, save metadata
                    meta_file = os.path.join(images_dir, f"{photo['id']}_meta.json")
                    with open(meta_file, 'w') as f:
                        json.dump(photo, f, indent=2)
            else:
                print(f"  No images found for {keyword}")
                
    print("\nBatch processing completed.")

if __name__ == "__main__":
    main()
