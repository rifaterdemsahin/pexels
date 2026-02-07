
import os
import re
import argparse
import sys

def fix_naming(base_dir):
    print(f"Scanning {base_dir}...")
    if not os.path.exists(base_dir):
        print(f"Directory {base_dir} does not exist.")
        return

    # Walk through the directory
    for root, dirs, files in os.walk(base_dir):
        folder_name = os.path.basename(root)
        
        # Skip the base dir itself
        if root == base_dir:
            continue
            
        print(f"Processing folder: {folder_name}")
        
        for file in files:
            # Check if file is already prefixed
            if file.startswith(f"{folder_name}_"):
                # print(f"  Skipping correct file: {file}")
                continue
                
            # Construct new filename
            new_name = f"{folder_name}_{file}"
            old_path = os.path.join(root, file)
            new_path = os.path.join(root, new_name)
            
            # Rename
            try:
                os.rename(old_path, new_path)
                print(f"  Renamed: {file} -> {new_name}")
            except OSError as e:
                print(f"  Error renaming {file}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Fix Asset Naming in Stock Folders")
    parser.add_argument("target_dir", help="Base directory containing StockVideos and StockImages folders (e.g. 3_Simulation/WeekX)")
    args = parser.parse_args()
    
    project_root = os.path.abspath(args.target_dir)
    
    stock_videos = os.path.join(project_root, 'StockVideos')
    stock_images = os.path.join(project_root, 'StockImages')
    
    if os.path.exists(stock_videos):
        fix_naming(stock_videos)
    else:
        print(f"Warning: {stock_videos} not found.")

    if os.path.exists(stock_images):
        fix_naming(stock_images)
    else:
        print(f"Warning: {stock_images} not found.")

if __name__ == "__main__":
    main()
