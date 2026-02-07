#!/usr/bin/env python3
"""
Pexels Stock Photo Generator
This script fetches stock photos from the Pexels API.
"""

import sys
import os
from pexels_video_fetcher import PexelsVideoFetcher

class PexelsPhotoFetcher(PexelsVideoFetcher):
    """
    Handles fetching photos from the Pexels API.
    Inherits from PexelsVideoFetcher to reuse authentication and base methods.
    """
    
    def search_photos(self, query, per_page=15, page=1, orientation=None, size=None, color=None):
        """
        Search for photos on Pexels.
        Wrapper around the parent method for clarity.
        """
        return super().search_photos(query, per_page, page, orientation, size, color)

def main():
    """Main function to demonstrate the Pexels Photo Fetcher."""
    try:
        fetcher = PexelsPhotoFetcher()
        
        print("Pexels Stock Photo Generator")
        print("================================\n")
        
        # Example 1: Search for photos
        query = "office"
        print(f"Searching for '{query}' photos...")
        results = fetcher.search_photos(query, per_page=5, orientation='landscape')
        
        if results and results.get('photos'):
            print(f"\nFound {results.get('total_results')} total results")
            print(f"Showing {len(results.get('photos'))} photos:\n")
            
            for photo in results['photos']:
                fetcher.display_photo_info(photo)
        else:
            print("No photos found or error occurred.")
            
    except ValueError as e:
        print(f"\nError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
