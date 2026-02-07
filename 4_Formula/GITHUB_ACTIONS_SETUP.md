# GitHub Actions Configuration for Pexels API

## Setting up the API Key as a GitHub Secret

To use the Pexels API in GitHub Actions workflows, you need to add your API key as a secret:

### Steps to Add Secret

1. Go to your GitHub repository
2. Click on **Settings**
3. In the left sidebar, click on **Secrets and variables** > **Actions**
4. Click **New repository secret**
5. Add the following secret:
   - **Name**: `PEXELS_API_KEY`
   - **Value**: Your Pexels API key from <https://www.pexels.com/api/>

### Using the Secret in Workflows

To use the secret in a GitHub Actions workflow, reference it like this:

```yaml
name: Test Pexels API

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run Pexels API script
        env:
          PEXELS_API_KEY: ${{ secrets.PEXELS_API_KEY }}
        run: |
          python 5_Symbols/pexels_video_fetcher.py
```

## Security Best Practices

1. **Never commit your API key to the repository**
2. **Always use the `.env` file locally** (which is git-ignored)
3. **Use GitHub Secrets for CI/CD pipelines**
4. **Rotate your API key if it's accidentally exposed**
5. **Limit API key permissions** if possible

## Environment Variables

The script looks for the API key in the following order:

1. Constructor parameter (if provided)
2. `PEXELS_API_KEY` environment variable
3. `.env` file (loaded automatically by python-dotenv)
