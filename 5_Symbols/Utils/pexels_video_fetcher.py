#!/usr/bin/env python3
"""
Pexels Stock Footage Generator
This script fetches stock video footage from the Pexels API.
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class PexelsVideoFetcher:
    """Handles fetching videos from the Pexels API."""
    
    BASE_URL = "https://api.pexels.com"
    
    def __init__(self, api_key=None):
        """
        Initialize the Pexels Video Fetcher.
        
        Args:
            api_key (str): Pexels API key. If not provided, will try to load from environment.
        """
        self.api_key = api_key or os.getenv('PEXELS_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "Pexels API key is required. "
                "Set PEXELS_API_KEY environment variable or pass it to the constructor."
            )
        
        self.headers = {
            'Authorization': self.api_key
        }
    
    def search_videos(self, query, per_page=15, page=1, orientation=None, size=None):
        """
        Search for videos on Pexels.
        
        Args:
            query (str): Search query (e.g., 'nature', 'city', 'ocean')
            per_page (int): Number of results per page (default: 15, max: 80)
            page (int): Page number (default: 1)
            orientation (str): Filter by orientation ('landscape', 'portrait', or 'square')
            size (str): Filter by size ('large', 'medium', or 'small')
            
        Returns:
            dict: API response containing video results
        """
        url = f"{self.BASE_URL}/videos/search"
        params = {
            'query': query,
            'per_page': per_page,
            'page': page
        }
        
        if orientation:
            params['orientation'] = orientation
        if size:
            params['size'] = size
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching videos: {e}")
            return None

    def search_photos(self, query, per_page=15, page=1, orientation=None, size=None, color=None):
        """
        Search for photos on Pexels.
        
        Args:
            query (str): Search query
            per_page (int): Number of results per page (default: 15, max: 80)
            page (int): Page number (default: 1)
            orientation (str): 'landscape', 'portrait', or 'square'
            size (str): 'large', 'medium', or 'small'
            color (str): 'red', 'orange', 'yellow', etc. or hex code
            
        Returns:
            dict: API response containing photo results
        """
        url = "https://api.pexels.com/v1/search" # Photo API endpoint is different base usually v1
        params = {
            'query': query,
            'per_page': per_page,
            'page': page
        }
        
        if orientation:
            params['orientation'] = orientation
        if size:
            params['size'] = size
        if color:
            params['color'] = color
            
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching photos: {e}")
            return None
    
    def get_popular_videos(self, per_page=15, page=1):
        """
        Get popular/curated videos from Pexels.
        
        Args:
            per_page (int): Number of results per page (default: 15, max: 80)
            page (int): Page number (default: 1)
            
        Returns:
            dict: API response containing popular video results
        """
        url = f"{self.BASE_URL}/videos/popular"
        params = {
            'per_page': per_page,
            'page': page
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching popular videos: {e}")
            return None
    
    def get_video_by_id(self, video_id):
        """
        Get a specific video by its ID.
        
        Args:
            video_id (int): The Pexels video ID
            
        Returns:
            dict: API response containing video details
        """
        url = f"{self.BASE_URL}/videos/{video_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching video: {e}")
            return None
    
    def display_video_info(self, video):
        """
        Display formatted information about a video.
        
        Args:
            video (dict): Video data from API response
        """
        print(f"\n{'='*60}")
        print(f"Video ID: {video.get('id')}")
        print(f"Duration: {video.get('duration')} seconds")
        print(f"Width: {video.get('width')}px")
        print(f"Height: {video.get('height')}px")
        print(f"User: {video.get('user', {}).get('name')}")
        print(f"URL: {video.get('url')}")
        
        video_files = video.get('video_files', [])
        if video_files:
            print("\nAvailable Files:")
            for i, vf in enumerate(video_files[:3], 1):  # Show first 3 files
                print(f"  {i}. Quality: {vf.get('quality')}, "
                      f"Width: {vf.get('width')}px, "
                      f"Link: {vf.get('link')}")
        print(f"{'='*60}\n")

    def display_photo_info(self, photo):
        """
        Display formatted information about a photo.
        
        Args:
            photo (dict): Photo data from API response
        """
        print(f"\n{'='*60}")
        print(f"Photo ID: {photo.get('id')}")
        print(f"Width: {photo.get('width')}px")
        print(f"Height: {photo.get('height')}px")
        print(f"Photographer: {photo.get('photographer')}")
        print(f"URL: {photo.get('url')}")
        print(f"Src Original: {photo.get('src', {}).get('original')}")
        print(f"{'='*60}\n")


def main():
    """Main function to demonstrate the Pexels Video Fetcher."""
    try:
        fetcher = PexelsVideoFetcher()
        
        print("Pexels Stock Footage Generator")
        print("================================\n")
        
        # Example 1: Search for videos
        query = "nature"
        print(f"Searching for '{query}' videos...")
        results = fetcher.search_videos(query, per_page=5)
        
        if results and results.get('videos'):
            print(f"\nFound {results.get('total_results')} total results")
            print(f"Showing {len(results.get('videos'))} videos:\n")
            
            for video in results['videos']:
                fetcher.display_video_info(video)
        else:
            print("No videos found or error occurred.")
        
        # Example 2: Get popular videos
        print("\n\nFetching popular videos...")
        popular = fetcher.get_popular_videos(per_page=3)
        
        if popular and popular.get('videos'):
            print(f"\nShowing {len(popular.get('videos'))} popular videos:\n")
            
            for video in popular['videos']:
                fetcher.display_video_info(video)
        else:
            print("No popular videos found or error occurred.")
        
    except ValueError as e:
        print(f"\nError: {e}")
        print("\nPlease ensure you have:")
        print("1. Created a .env file with your PEXELS_API_KEY")
        print("2. Or set the PEXELS_API_KEY environment variable")
        print("3. Get your API key from: https://www.pexels.com/api/")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
