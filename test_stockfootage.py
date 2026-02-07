#!/usr/bin/env python3
"""
Test script for Pexels Stock Footage functionality.
This script tests the API integration and core functionality.
"""

import os
import sys
from pexels_video_fetcher import PexelsVideoFetcher


def test_api_connection():
    """Test that API connection works with the provided key."""
    print("Test 1: API Connection")
    print("-" * 50)
    try:
        fetcher = PexelsVideoFetcher()
        print("✓ API key loaded successfully")
        return True
    except ValueError as e:
        print(f"✗ Failed to load API key: {e}")
        return False


def test_search_videos():
    """Test video search functionality."""
    print("\nTest 2: Search Videos")
    print("-" * 50)
    try:
        fetcher = PexelsVideoFetcher()
        results = fetcher.search_videos("nature", per_page=5)
        
        if results and results.get('videos'):
            print(f"✓ Search successful: Found {results.get('total_results')} total results")
            print(f"✓ Retrieved {len(results.get('videos'))} videos")
            
            # Verify video structure
            video = results['videos'][0]
            required_fields = ['id', 'width', 'height', 'url', 'duration']
            for field in required_fields:
                if field not in video:
                    print(f"✗ Missing required field: {field}")
                    return False
            print("✓ Video structure is valid")
            return True
        else:
            print("✗ Search failed: No results returned")
            return False
    except Exception as e:
        print(f"✗ Search failed with error: {e}")
        return False


def test_get_popular_videos():
    """Test popular videos functionality."""
    print("\nTest 3: Get Popular Videos")
    print("-" * 50)
    try:
        fetcher = PexelsVideoFetcher()
        results = fetcher.get_popular_videos(per_page=3)
        
        if results and results.get('videos'):
            print(f"✓ Popular videos retrieved: {len(results.get('videos'))} videos")
            return True
        else:
            print("✗ Failed to get popular videos")
            return False
    except Exception as e:
        print(f"✗ Failed with error: {e}")
        return False


def test_get_video_by_id():
    """Test getting a specific video by ID."""
    print("\nTest 4: Get Video by ID")
    print("-" * 50)
    try:
        fetcher = PexelsVideoFetcher()
        # First, get a video ID from search results
        results = fetcher.search_videos("nature", per_page=1)
        
        if not results or not results.get('videos'):
            print("✗ Could not get test video ID")
            return False
        
        video_id = results['videos'][0]['id']
        video = fetcher.get_video_by_id(video_id)
        
        if video and video.get('id') == video_id:
            print(f"✓ Successfully retrieved video with ID {video_id}")
            return True
        else:
            print(f"✗ Failed to retrieve video with ID {video_id}")
            return False
    except Exception as e:
        print(f"✗ Failed with error: {e}")
        return False


def test_filtered_search():
    """Test search with filters."""
    print("\nTest 5: Filtered Search")
    print("-" * 50)
    try:
        fetcher = PexelsVideoFetcher()
        results = fetcher.search_videos(
            query="ocean",
            per_page=3,
            orientation="landscape"
        )
        
        if results and results.get('videos'):
            print(f"✓ Filtered search successful: {len(results.get('videos'))} videos")
            return True
        else:
            print("✗ Filtered search failed")
            return False
    except Exception as e:
        print(f"✗ Failed with error: {e}")
        return False


def main():
    """Run all tests and report results."""
    print("=" * 50)
    print("Pexels Stock Footage Test Suite")
    print("=" * 50)
    print()
    
    # Check if API key is available
    api_key = os.getenv('PEXELS_API_KEY')
    if not api_key:
        print("ERROR: PEXELS_API_KEY environment variable is not set!")
        print("\nPlease ensure you have:")
        print("1. Created a .env file with PEXELS_API_KEY")
        print("2. Or set the PEXELS_API_KEY environment variable")
        print("3. For GitHub Actions: Add PEXELS_API_KEY as a repository secret")
        print("   https://github.com/rifaterdemsahin/pexels/settings/secrets/actions")
        sys.exit(1)
    
    print(f"API Key: {'*' * (len(api_key) - 4)}{api_key[-4:]}\n")
    
    # Run all tests
    tests = [
        test_api_connection,
        test_search_videos,
        test_get_popular_videos,
        test_get_video_by_id,
        test_filtered_search
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test crashed: {e}")
            results.append(False)
    
    # Print summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
