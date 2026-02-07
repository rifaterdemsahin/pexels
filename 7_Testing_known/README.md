# 7_Testing_known - Validation

Contains test plans, validation procedures, and acceptance criteria for ensuring application quality to reach the objectives in real and reach a known world.

## Sample Test Run

A sample test script `sample_test_run.py` is included to validate the core functionality of the Pexels Video Fetcher.

### Running the Test

Run the following command from the project root:

```bash
python 7_Testing_known/sample_test_run.py
```

### Test Coverage

The sample test covers:

1. **API Authentication**: Verifies that the `.env` file is loaded and the API key is valid.
2. **Search Functionality**: Performs a search for "nature" and verifies results are returned.
3. **Popular Videos**: Fetches popular videos to ensure that endpoint is working.

### Expected Output

```text
2026-02-07 05:13:34,731 - INFO - Loaded environment variables from C:\projects\pexels\5_Symbols\.env
2026-02-07 05:13:34,734 - INFO - Testing search_videos with query 'nature'...
2026-02-07 05:13:35,429 - INFO - Found video: ID=28379894, URL=https://www.pexels.com/video/a-small-stream-in-the-jungle-with-green-plants-28379894/
2026-02-07 05:13:35,434 - INFO - Testing get_popular_videos...
Ran 2 tests in 0.896s
OK
```
