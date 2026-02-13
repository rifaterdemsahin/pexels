#!/usr/bin/env python3
"""
Demo Asset Generator - Creates placeholder files for testing
This script creates demo/placeholder files to show the expected output structure
without requiring a Pexels API key.
"""

import os
import json
import yaml

def create_placeholder_video(filepath, video_id, name, search_query):
    """Create a placeholder video file."""
    # Create a minimal MP4 header (this is not a real video, just a placeholder)
    placeholder_content = f"PLACEHOLDER VIDEO: {video_id} - {name}\nSearch Query: {search_query}\n"
    with open(filepath, 'w') as f:
        f.write(placeholder_content)
    print(f"  ✓ Created placeholder: {os.path.basename(filepath)}")

def create_placeholder_image(filepath, image_id, name, prompt):
    """Create a placeholder image file."""
    placeholder_content = f"PLACEHOLDER IMAGE: {image_id} - {name}\nPrompt: {prompt}\n"
    with open(filepath, 'w') as f:
        f.write(placeholder_content)
    print(f"  ✓ Created placeholder: {os.path.basename(filepath)}")

def create_metadata(filepath, config_data, asset_type="video"):
    """Create a metadata JSON file."""
    metadata = {
        "config_id": config_data.get("id"),
        "config_name": config_data.get("name"),
        "priority": config_data.get("priority"),
        "asset_type": asset_type,
        "note": "This is a placeholder file for demonstration purposes",
    }
    
    if asset_type == "video":
        metadata["search_query"] = config_data.get("search_query")
    else:
        metadata["prompt"] = config_data.get("prompt", "")[:100]
    
    with open(filepath, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"  ✓ Created metadata: {os.path.basename(filepath)}")

def main():
    """Create demo placeholder files."""
    print("=" * 60)
    print("Demo Asset Generator - Creating Placeholder Files")
    print("=" * 60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, 'input')
    output_dir = os.path.join(script_dir, 'output')
    
    videos_dir = os.path.join(output_dir, 'StockVideos')
    images_dir = os.path.join(output_dir, 'StockImages')
    
    os.makedirs(videos_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    
    print(f"\nOutput directory: {output_dir}\n")
    
    # Load and process videos
    yaml_path = os.path.join(input_dir, 'batch_generation_data.yaml')
    if os.path.exists(yaml_path):
        print("Processing Videos...")
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)
            video_config = config.get('video', [])
            
            for i, video in enumerate(video_config, 1):
                video_id = video.get('id', f'video_{i}')
                name = video.get('name', 'unnamed')
                search_query = video.get('search_query', '')
                
                print(f"\n[{i}/{len(video_config)}] {video_id} - {name}")
                
                # Create placeholder video file
                video_file = os.path.join(videos_dir, f"{video_id}.mp4")
                create_placeholder_video(video_file, video_id, name, search_query)
                
                # Create metadata file
                meta_file = os.path.join(videos_dir, f"{video_id}_meta.json")
                create_metadata(meta_file, video, "video")
    
    # Load and process images from assets_config.json
    assets_path = os.path.join(input_dir, 'assets_config.json')
    image_configs = []
    
    if os.path.exists(assets_path):
        with open(assets_path, 'r') as f:
            assets = json.load(f)
            image_configs.extend(assets.get('images', []))
    
    # Load and process icons
    icons_path = os.path.join(input_dir, 'icons.json')
    if os.path.exists(icons_path):
        with open(icons_path, 'r') as f:
            icons = json.load(f)
            if isinstance(icons, list):
                image_configs.extend(icons)
    
    if image_configs:
        print(f"\n{'='*60}")
        print("Processing Images...")
        print(f"{'='*60}")
        
        for i, image in enumerate(image_configs, 1):
            image_id = image.get('id', f'image_{i}')
            name = image.get('name', 'unnamed')
            prompt = image.get('prompt', '')
            
            print(f"\n[{i}/{len(image_configs)}] {image_id} - {name}")
            
            # Create placeholder image file
            image_file = os.path.join(images_dir, f"{image_id}.jpg")
            create_placeholder_image(image_file, image_id, name, prompt)
            
            # Create metadata file
            meta_file = os.path.join(images_dir, f"{image_id}_meta.json")
            create_metadata(meta_file, image, "image")
    
    print(f"\n{'='*60}")
    print("Demo files created successfully!")
    print(f"{'='*60}")
    print(f"\nCheck the output directories:")
    print(f"  - {videos_dir}")
    print(f"  - {images_dir}")
    print("\nNote: These are placeholder files for demonstration.")
    print("Run process_assets.py with a Pexels API key to fetch real assets.")

if __name__ == "__main__":
    main()
