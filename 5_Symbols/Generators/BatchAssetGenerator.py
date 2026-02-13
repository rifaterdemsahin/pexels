#!/usr/bin/env python3
"""
Batch Asset Generator
Reads batch_generation_data.yaml, assets_config.json, and icons.json,
then fetches real video and image assets from the Pexels API.

Usage:
    python BatchAssetGenerator.py --config <path/to/batch_generation_data.yaml> --output-dir <output_path>
    
    # Or with extra image sources:
    python BatchAssetGenerator.py --config <yaml> --output-dir <out> \
        --assets-config <assets_config.json> --icons <icons.json>
"""

import os
import sys
import yaml
import json
import argparse
import requests
from pathlib import Path

# Add Utils directory to path to import helpers
utils_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Utils'))
if utils_path not in sys.path:
    sys.path.append(utils_path)

try:
    from pexels_video_fetcher import PexelsVideoFetcher
except ImportError:
    print(f"Error: Could not import PexelsVideoFetcher from {utils_path}")
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
        print(f"    File already exists at {filepath}")
        return True

    print(f"    Downloading to {filepath}...")
    try:
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("    ✓ Download complete.")
        return True
    except Exception as e:
        print(f"    ✗ Error downloading: {e}")
        return False


def process_videos(video_config, fetcher, videos_dir):
    """Fetch and download videos from Pexels based on search_query."""
    if not video_config:
        print("No video entries to process.")
        return 0, 0

    os.makedirs(videos_dir, exist_ok=True)
    success, failed = 0, 0

    for i, entry in enumerate(video_config, 1):
        video_id = entry.get('id', f'video_{i}')
        name = entry.get('name', 'unnamed')
        search_query = entry.get('search_query', '')
        priority = entry.get('priority', 'MEDIUM')

        print(f"\n  [{i}/{len(video_config)}] {video_id} - {name} (Priority: {priority})")
        print(f"    Search: '{search_query}'")

        if not search_query:
            print(f"    ⚠ No search_query, skipping...")
            failed += 1
            continue

        results = fetcher.search_videos(search_query, per_page=1, orientation='landscape')

        if results and results.get('videos'):
            video = results['videos'][0]
            pexels_id = video.get('id')
            print(f"    Found Pexels video ID: {pexels_id}")

            # Download best quality video
            video_files = video.get('video_files', [])
            downloaded = False
            if video_files:
                # Prefer HD (1920 width) or best available
                video_files.sort(key=lambda x: x.get('width', 0), reverse=True)
                # Try to find a reasonable size (not too huge)
                selected = None
                for vf in video_files:
                    w = vf.get('width', 0)
                    if 720 <= w <= 1920:
                        selected = vf
                        break
                if not selected:
                    selected = video_files[0]

                download_url = selected.get('link')
                if download_url:
                    filepath = os.path.join(videos_dir, f"{video_id}.mp4")
                    downloaded = download_file(download_url, filepath)

            # Save metadata
            meta = {
                'config_id': video_id,
                'config_name': name,
                'search_query': search_query,
                'priority': priority,
                'scene': entry.get('scene', ''),
                'pexels_video_id': pexels_id,
                'pexels_url': video.get('url', ''),
                'pexels_video': video
            }
            meta_path = os.path.join(videos_dir, f"{video_id}_meta.json")
            with open(meta_path, 'w') as f:
                json.dump(meta, f, indent=2)
            print(f"    ✓ Metadata saved: {video_id}_meta.json")

            if downloaded:
                success += 1
            else:
                failed += 1
        else:
            print(f"    ✗ No videos found for '{search_query}'")
            failed += 1

    return success, failed


def process_images(image_configs, fetcher, images_dir):
    """Fetch and download images from Pexels based on search_query or prompt."""
    if not image_configs:
        print("No image entries to process.")
        return 0, 0

    os.makedirs(images_dir, exist_ok=True)
    success, failed = 0, 0

    for i, entry in enumerate(image_configs, 1):
        image_id = entry.get('id', f'image_{i}')
        name = entry.get('name', 'unnamed')
        prompt = entry.get('prompt', '')
        priority = entry.get('priority', 'MEDIUM')

        # Use search_query if provided, else extract from prompt
        search_query = entry.get('search_query', '')
        if not search_query and prompt:
            search_query = ' '.join(prompt.split()[:5])

        print(f"\n  [{i}/{len(image_configs)}] {image_id} - {name} (Priority: {priority})")
        print(f"    Search: '{search_query}'")

        if not search_query:
            print(f"    ⚠ No search query, skipping...")
            failed += 1
            continue

        # Determine orientation based on image_size if present
        orientation = 'landscape'
        img_size = entry.get('image_size', {})
        if img_size:
            w = img_size.get('width', 0)
            h = img_size.get('height', 0)
            if w and h:
                if w == h:
                    orientation = 'square'
                elif h > w:
                    orientation = 'portrait'

        results = fetcher.search_photos(search_query, per_page=1, orientation=orientation)

        if results and results.get('photos'):
            photo = results['photos'][0]
            pexels_id = photo.get('id')
            print(f"    Found Pexels photo ID: {pexels_id}")

            # Download original photo
            download_url = photo.get('src', {}).get('original')
            downloaded = False
            if download_url:
                filepath = os.path.join(images_dir, f"{image_id}.jpg")
                downloaded = download_file(download_url, filepath)

            # Save metadata
            meta = {
                'config_id': image_id,
                'config_name': name,
                'prompt': prompt,
                'search_query': search_query,
                'priority': priority,
                'scene': entry.get('scene', ''),
                'pexels_photo_id': pexels_id,
                'pexels_url': photo.get('url', ''),
                'photographer': photo.get('photographer', ''),
                'pexels_photo': photo
            }
            meta_path = os.path.join(images_dir, f"{image_id}_meta.json")
            with open(meta_path, 'w') as f:
                json.dump(meta, f, indent=2)
            print(f"    ✓ Metadata saved: {image_id}_meta.json")

            if downloaded:
                success += 1
            else:
                failed += 1
        else:
            print(f"    ✗ No photos found for '{search_query}'")
            failed += 1

    return success, failed


def main():
    parser = argparse.ArgumentParser(
        description="Batch Asset Generator - Download stock footage from Pexels"
    )
    parser.add_argument("--config", required=True,
                        help="Path to batch_generation_data.yaml")
    parser.add_argument("--output-dir", required=True,
                        help="Base output directory (will create StockVideos/ and StockImages/ inside)")
    parser.add_argument("--assets-config", default=None,
                        help="Optional path to assets_config.json for additional images")
    parser.add_argument("--icons", default=None,
                        help="Optional path to icons.json for icon images")
    args = parser.parse_args()

    config_path = args.config
    output_dir = args.output_dir
    videos_dir = os.path.join(output_dir, 'StockVideos')
    images_dir = os.path.join(output_dir, 'StockImages')

    print("=" * 60)
    print("Batch Asset Generator - Pexels Downloader")
    print("=" * 60)

    # Load YAML config
    print(f"\nLoading config: {config_path}")
    yaml_config = load_yaml(config_path)
    if not yaml_config:
        print("Failed to load config. Exiting.")
        sys.exit(1)

    video_config = yaml_config.get('video', [])
    image_config = list(yaml_config.get('images', []))
    print(f"  ✓ {len(video_config)} videos from YAML")
    print(f"  ✓ {len(image_config)} images from YAML")

    # Load additional image sources (deduplicate by ID)
    existing_ids = {img.get('id') for img in image_config}

    if args.assets_config:
        assets_data = load_json(args.assets_config)
        if assets_data:
            new_imgs = [img for img in assets_data.get('images', [])
                        if img.get('id') not in existing_ids]
            image_config.extend(new_imgs)
            existing_ids.update(img.get('id') for img in new_imgs)
            print(f"  ✓ {len(new_imgs)} unique images from assets_config.json")

    if args.icons:
        icons_data = load_json(args.icons)
        if icons_data and isinstance(icons_data, list):
            new_icons = [icon for icon in icons_data
                         if icon.get('id') not in existing_ids]
            image_config.extend(new_icons)
            print(f"  ✓ {len(new_icons)} icons from icons.json")

    # Initialize Pexels Fetcher
    try:
        fetcher = PexelsVideoFetcher()
        print("\n✓ Pexels API initialized")
    except ValueError as e:
        print(f"\n✗ Error: {e}")
        print("Set PEXELS_API_KEY in .env or environment variable.")
        sys.exit(1)

    # Process Videos
    print(f"\n{'=' * 60}")
    print(f"DOWNLOADING VIDEOS ({len(video_config)} entries)")
    print(f"{'=' * 60}")
    v_ok, v_fail = process_videos(video_config, fetcher, videos_dir)

    # Process Images
    print(f"\n{'=' * 60}")
    print(f"DOWNLOADING IMAGES ({len(image_config)} entries)")
    print(f"{'=' * 60}")
    i_ok, i_fail = process_images(image_config, fetcher, images_dir)

    # Summary
    print(f"\n{'=' * 60}")
    print("DOWNLOAD SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Videos: {v_ok} downloaded, {v_fail} failed/skipped")
    print(f"  Images: {i_ok} downloaded, {i_fail} failed/skipped")
    print(f"  Output: {output_dir}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
