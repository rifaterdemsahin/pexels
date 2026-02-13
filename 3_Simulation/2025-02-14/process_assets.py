#!/usr/bin/env python3
"""
Asset Processing Script for 2025-02-14
Processes input files and fetches stock videos and photos from Pexels API.
"""

import os
import sys
import yaml
import json
import requests
from pathlib import Path

# Add Utils directory to path to import Pexels fetcher
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
utils_path = os.path.join(repo_root, '5_Symbols', 'Utils')
if utils_path not in sys.path:
    sys.path.append(utils_path)

try:
    from pexels_video_fetcher import PexelsVideoFetcher
except ImportError as e:
    print(f"Error: Could not import PexelsVideoFetcher from {utils_path}")
    print(f"Details: {e}")
    print("Ensure 5_Symbols/Utils/pexels_video_fetcher.py exists.")
    sys.exit(1)

def load_yaml(filepath):
    """Load a YAML file."""
    if not os.path.exists(filepath):
        print(f"Warning: File not found: {filepath}")
        return None
    
    with open(filepath, 'r') as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML {filepath}: {e}")
            return None

def load_json(filepath):
    """Load a JSON file."""
    if not os.path.exists(filepath):
        print(f"Warning: File not found: {filepath}")
        return None
    
    with open(filepath, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON {filepath}: {e}")
            return None

def download_file(url, filepath):
    """Downloads a file from a URL to the specified filepath."""
    if os.path.exists(filepath):
        print(f"    File already exists: {filepath}")
        return True

    print(f"    Downloading to: {filepath}")
    try:
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"    ✓ Download complete")
        return True
    except Exception as e:
        print(f"    ✗ Error downloading: {e}")
        return False

def process_videos(video_config, fetcher, output_dir):
    """Process video entries from the YAML configuration."""
    if not video_config:
        print("No video configuration found.")
        return
    
    print(f"\n{'='*60}")
    print("PROCESSING VIDEOS")
    print(f"{'='*60}")
    
    videos_dir = os.path.join(output_dir, 'StockVideos')
    os.makedirs(videos_dir, exist_ok=True)
    
    for i, video_entry in enumerate(video_config, 1):
        video_id = video_entry.get('id', f'video_{i}')
        name = video_entry.get('name', 'unnamed')
        search_query = video_entry.get('search_query', '')
        priority = video_entry.get('priority', 'MEDIUM')
        
        print(f"\n[{i}/{len(video_config)}] Processing: {video_id} - {name}")
        print(f"  Priority: {priority}")
        print(f"  Search query: '{search_query}'")
        
        if not search_query:
            print(f"  ⚠ No search query provided, skipping...")
            continue
        
        # Search for videos using the search_query
        results = fetcher.search_videos(
            search_query, 
            per_page=1, 
            orientation='landscape'
        )
        
        if results and results.get('videos'):
            video = results['videos'][0]
            print(f"  ✓ Found video ID: {video.get('id')}")
            
            # Get the best quality video file
            video_files = video.get('video_files', [])
            if video_files:
                # Sort by width to get best quality
                video_files.sort(key=lambda x: x.get('width', 0), reverse=True)
                best_video = video_files[0]
                download_url = best_video.get('link')
                
                if download_url:
                    # Create filename based on video_id from config
                    filename = f"{video_id}.mp4"
                    filepath = os.path.join(videos_dir, filename)
                    download_file(download_url, filepath)
                    
                    # Save metadata
                    meta_filename = f"{video_id}_meta.json"
                    meta_filepath = os.path.join(videos_dir, meta_filename)
                    with open(meta_filepath, 'w') as f:
                        json.dump({
                            'config_id': video_id,
                            'config_name': name,
                            'search_query': search_query,
                            'priority': priority,
                            'pexels_video': video
                        }, f, indent=2)
                    print(f"    ✓ Metadata saved: {meta_filename}")
        else:
            print(f"  ✗ No videos found for query: '{search_query}'")

def process_images(image_configs, fetcher, output_dir):
    """Process image entries from JSON configurations."""
    if not image_configs:
        print("No image configuration found.")
        return
    
    print(f"\n{'='*60}")
    print("PROCESSING IMAGES")
    print(f"{'='*60}")
    
    images_dir = os.path.join(output_dir, 'StockImages')
    os.makedirs(images_dir, exist_ok=True)
    
    for i, image_entry in enumerate(image_configs, 1):
        image_id = image_entry.get('id', f'image_{i}')
        name = image_entry.get('name', 'unnamed')
        prompt = image_entry.get('prompt', '')
        priority = image_entry.get('priority', 'MEDIUM')
        
        print(f"\n[{i}/{len(image_configs)}] Processing: {image_id} - {name}")
        print(f"  Priority: {priority}")
        # Display prompt with smart truncation
        if len(prompt) > 80:
            print(f"  Prompt: '{prompt[:80]}...'")
        else:
            print(f"  Prompt: '{prompt}'")
        
        # Use search_query from config if available, otherwise extract from prompt
        search_query = image_entry.get('search_query', '')
        if not search_query:
            # Simple heuristic: use first few meaningful words from prompt
            search_query = ' '.join(prompt.split()[:5])
        print(f"  Search query: '{search_query}'")
        
        # Search for photos
        results = fetcher.search_photos(
            search_query,
            per_page=1,
            orientation='landscape'
        )
        
        if results and results.get('photos'):
            photo = results['photos'][0]
            print(f"  ✓ Found photo ID: {photo.get('id')}")
            
            # Download the original photo
            download_url = photo.get('src', {}).get('original')
            if download_url:
                # Create filename based on image_id from config
                filename = f"{image_id}.jpg"
                filepath = os.path.join(images_dir, filename)
                download_file(download_url, filepath)
                
                # Save metadata
                meta_filename = f"{image_id}_meta.json"
                meta_filepath = os.path.join(images_dir, meta_filename)
                with open(meta_filepath, 'w') as f:
                    json.dump({
                        'config_id': image_id,
                        'config_name': name,
                        'prompt': prompt,
                        'priority': priority,
                        'pexels_photo': photo
                    }, f, indent=2)
                print(f"    ✓ Metadata saved: {meta_filename}")
        else:
            print(f"  ✗ No photos found for query: '{search_query}'")

def main():
    """Main function to process all assets."""
    print("=" * 60)
    print("Pexels Asset Processing Script")
    print("2025-02-14 Input/Output Processing")
    print("=" * 60)
    
    # Define paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, 'input')
    output_dir = os.path.join(script_dir, 'output')
    
    print(f"\nInput directory:  {input_dir}")
    print(f"Output directory: {output_dir}")
    
    # Initialize Pexels Fetcher
    try:
        fetcher = PexelsVideoFetcher()
        print("\n✓ Pexels API initialized successfully")
    except ValueError as e:
        print(f"\n✗ Error initializing Pexels API: {e}")
        print("\nPlease ensure you have:")
        print("1. Created a .env file with your PEXELS_API_KEY")
        print("2. Or set the PEXELS_API_KEY environment variable")
        print("3. Get your API key from: https://www.pexels.com/api/")
        sys.exit(1)
    
    # Load configuration files
    print("\nLoading configuration files...")
    
    # 1. Load batch_generation_data.yaml for videos
    yaml_path = os.path.join(input_dir, 'batch_generation_data.yaml')
    yaml_config = load_yaml(yaml_path)
    video_config = yaml_config.get('video', []) if yaml_config else []
    print(f"  ✓ Loaded {len(video_config)} video entries from batch_generation_data.yaml")
    
    # 2. Load images from batch_generation_data.yaml
    yaml_images = yaml_config.get('images', []) if yaml_config else []
    image_config = list(yaml_images)
    print(f"  ✓ Loaded {len(yaml_images)} image entries from batch_generation_data.yaml")
    
    # 3. Load assets_config.json for images
    assets_json_path = os.path.join(input_dir, 'assets_config.json')
    assets_config = load_json(assets_json_path)
    if assets_config:
        existing_ids = {img.get('id') for img in image_config}
        assets_images = [img for img in assets_config.get('images', []) if img.get('id') not in existing_ids]
        image_config.extend(assets_images)
        print(f"  ✓ Loaded {len(assets_images)} unique image entries from assets_config.json")
    
    # 4. Load icons.json for icon images
    icons_json_path = os.path.join(input_dir, 'icons.json')
    icons_config = load_json(icons_json_path)
    if icons_config and isinstance(icons_config, list):
        existing_ids = {img.get('id') for img in image_config}
        new_icons = [icon for icon in icons_config if icon.get('id') not in existing_ids]
        image_config.extend(new_icons)
        print(f"  ✓ Loaded {len(new_icons)} icon entries from icons.json")
    
    # Process videos
    if video_config:
        process_videos(video_config, fetcher, output_dir)
    
    # Process images
    if image_config:
        process_images(image_config, fetcher, output_dir)
    
    print(f"\n{'='*60}")
    print("PROCESSING COMPLETE")
    print(f"{'='*60}")
    print(f"\nOutput saved to: {output_dir}")
    print("  - StockVideos/")
    print("  - StockImages/")
    print("\nCheck the output directories for downloaded assets and metadata files.")

if __name__ == "__main__":
    main()
