
import os
import re

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
                print(f"  Skipping correct file: {file}")
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
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    stock_videos = os.path.join(project_root, '3_Simulation', 'Feb1', 'StockVideos')
    stock_images = os.path.join(project_root, '3_Simulation', 'Feb1', 'StockImages')
    
    fix_naming(stock_videos)
    fix_naming(stock_images)

if __name__ == "__main__":
    main()
