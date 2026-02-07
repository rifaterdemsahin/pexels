import sys
import os
import unittest
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Add 5_Symbols to path to import the module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../5_Symbols')))

try:
    from pexels_video_fetcher import PexelsVideoFetcher
except ImportError:
    logging.error("Could not import PexelsVideoFetcher. Make sure the file exists in 5_Symbols.")
    sys.exit(1)

from dotenv import load_dotenv

# Load env from 5_Symbols
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../5_Symbols/.env'))
if os.path.exists(env_path):
    load_dotenv(env_path)
    logging.info(f"Loaded environment variables from {env_path}")
else:
    logging.warning(f".env file not found at {env_path}. Relying on system environment variables.")

class TestPexelsFetcher(unittest.TestCase):
    def setUp(self):
        try:
            self.fetcher = PexelsVideoFetcher()
        except ValueError as e:
            self.fail(f"Failed to initialize fetcher: {e}")

    def test_search_videos(self):
        logging.info("Testing search_videos with query 'nature'...")
        results = self.fetcher.search_videos("nature", per_page=1)
        self.assertIsNotNone(results, "Search results should not be None")
        self.assertIn('videos', results, "Results should contain 'videos' key")
        self.assertTrue(len(results['videos']) > 0, "Should find at least one video")
        
        video = results['videos'][0]
        logging.info(f"Found video: ID={video.get('id')}, URL={video.get('url')}")

    def test_get_popular_videos(self):
        logging.info("Testing get_popular_videos...")
        results = self.fetcher.get_popular_videos(per_page=1)
        self.assertIsNotNone(results, "Popular results should not be None")
        self.assertIn('videos', results, "Results should contain 'videos' key")
        self.assertTrue(len(results['videos']) > 0, "Should find at least one popular video")

if __name__ == '__main__':
    unittest.main()
