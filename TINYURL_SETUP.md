# TinyURL API Setup Guide

This guide explains how to set up TinyURL API integration for the AI News Tweeter application.

## Overview

The application uses TinyURL to shorten long Google News URLs, reducing them from ~244 characters to ~28 characters. This helps keep tweets within Twitter's character limits while preserving link functionality.

## TinyURL API Options

The application supports two modes:

### 1. Authenticated API (Recommended)
- **Requires**: TinyURL API token
- **Benefits**: Higher rate limits, analytics, custom domains, reliability
- **Cost**: Free tier available with 1,000 URLs/month
- **Endpoint**: `https://api.tinyurl.com/create`

### 2. Free Fallback API
- **Requires**: No authentication
- **Benefits**: No setup required
- **Limitations**: Lower rate limits, no analytics
- **Endpoint**: `http://tinyurl.com/api-create.php`

## Setup Instructions

### Step 1: Get TinyURL API Token

1. Visit [TinyURL Developer Portal](https://tinyurl.com/app/dev)
2. Sign up for a free account or log in
3. Navigate to the API section
4. Click "Create API" to generate your API token
5. Copy the generated API token

### Step 2: Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your TinyURL API token:
   ```env
   # TinyURL API Configuration (Required for URL shortening)
   TINYURL_API_TOKEN=your_actual_tinyurl_api_token_here
   ```

### Step 3: Test the Integration

Run the test script to verify TinyURL integration:
```bash
python3 test_tinyurl.py
```

You should see output showing:
- Original URLs (~244 characters)
- Shortened URLs (~28 characters)
- Successful URL shortening logs

## Fallback Behavior

If no TinyURL API token is provided:
1. The application will log a warning
2. It will automatically fall back to the free TinyURL endpoint
3. URL shortening will still work, but with limitations

## API Rate Limits

### Free Tier (Authenticated)
- 1,000 URL shortenings per month
- Sufficient for most personal projects
- Includes basic analytics

### Free Endpoint (Unauthenticated)
- Lower rate limits (exact limits not published)
- No analytics or custom features

## Troubleshooting

### Common Issues

1. **"TinyURL API token not found" warning**
   - Solution: Add `TINYURL_API_TOKEN` to your `.env` file

2. **"TinyURL API returned status code: 401"**
   - Solution: Verify your API token is correct
   - Check that the token hasn't expired

3. **"Failed to shorten URL with TinyURL"**
   - The application will fall back to using original URLs
   - Check your internet connection
   - Verify the TinyURL service is operational

### Debug Logging

To see detailed TinyURL logs, the application includes:
- Debug logs for URL shortening attempts
- Info logs for successful shortenings
- Warning logs for failures with fallback behavior

## Security Best Practices

1. **Never commit API tokens to version control**
   - Always use `.env` files
   - Add `.env` to your `.gitignore`

2. **Rotate API tokens periodically**
   - Generate new tokens every few months
   - Update your `.env` file accordingly

3. **Monitor API usage**
   - Check your TinyURL dashboard for usage statistics
   - Set up alerts if approaching rate limits

## Integration Details

The TinyURL integration is implemented in `news_fetcher.py`:

- **Method**: `_shorten_url_with_tinyurl()`
- **Fallback**: Automatic fallback to free endpoint
- **Error Handling**: Graceful degradation to original URLs
- **Logging**: Comprehensive logging for debugging

## Cost Considerations

- **Free Tier**: 1,000 URLs/month should be sufficient for most use cases
- **Paid Plans**: Available for higher volume needs
- **Fallback**: Free endpoint available as backup

The application is designed to work reliably whether you use the authenticated API or the free fallback endpoint.