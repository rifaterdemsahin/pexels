#!/usr/bin/env python3
"""
Example script demonstrating how to use the Pexels Video Fetcher module.
"""

from pexels_video_fetcher import PexelsVideoFetcher

def example_search():
    """Example: Search for videos by keyword."""
    print("Example 1: Search for videos\n" + "="*50)
    
    fetcher = PexelsVideoFetcher()
    
    # Search for nature videos
    results = fetcher.search_videos("nature", per_page=5)
    
    if results and results.get('videos'):
        print(f"Found {results.get('total_results')} total results")
        print(f"Showing first {len(results.get('videos'))} videos:\n")
        
        for video in results['videos']:
            fetcher.display_video_info(video)
    else:
        print("No videos found.")
    print()


def example_popular():
    """Example: Get popular/curated videos."""
    print("\nExample 2: Get popular videos\n" + "="*50)
    
    fetcher = PexelsVideoFetcher()
    
    # Get popular videos
    results = fetcher.get_popular_videos(per_page=3)
    
    if results and results.get('videos'):
        print(f"Showing {len(results.get('videos'))} popular videos:\n")
        
        for video in results['videos']:
            fetcher.display_video_info(video)
    else:
        print("No popular videos found.")
    print()


def example_filtered_search():
    """Example: Search with filters."""
    print("\nExample 3: Search with filters\n" + "="*50)
    
    fetcher = PexelsVideoFetcher()
    
    # Search for landscape ocean videos
    results = fetcher.search_videos(
        query="ocean",
        per_page=5,
        orientation="landscape",
        size="large"
    )
    
    if results and results.get('videos'):
        print(f"Found {results.get('total_results')} landscape ocean videos")
        print(f"Showing first {len(results.get('videos'))} videos:\n")
        
        for video in results['videos']:
            fetcher.display_video_info(video)
    else:
        print("No videos found.")
    print()


def example_specific_video():
    """Example: Get a specific video by ID."""
    print("\nExample 4: Get specific video by ID\n" + "="*50)
    
    fetcher = PexelsVideoFetcher()
    
    # Get video with ID 2499611 (example ID)
    video_id = 2499611
    video = fetcher.get_video_by_id(video_id)
    
    if video:
        print(f"Video details for ID {video_id}:\n")
        fetcher.display_video_info(video)
    else:
        print(f"Video with ID {video_id} not found.")
    print()


if __name__ == "__main__":
    print("Pexels API Examples")
    print("=" * 50)
    print()
    
    try:
        # Run all examples
        example_search()
        example_popular()
        example_filtered_search()
        example_specific_video()
        
    except ValueError as e:
        print(f"\nError: {e}")
        print("\nPlease set up your API key first:")
        print("1. Copy .env.example to .env")
        print("2. Add your Pexels API key to the .env file")
        print("3. Get your API key from: https://www.pexels.com/api/")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
