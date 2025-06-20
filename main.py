#!/usr/bin/env python3
"""
Main orchestrator for AI News Tweeter
Fetches AI news, formats tweets, and posts them to Twitter
"""

import os
import sys
import logging
from datetime import datetime

from news_fetcher import NewsFetcher
from tweet_formatter import TweetFormatter
from tweet_poster import TweetPoster

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Enable debug logging to see URL extraction details
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tweet_log.txt'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main function to orchestrate the news tweeting process"""
    try:
        logger.info("Starting AI News Tweeter process")
        
        # Initialize components
        news_fetcher = NewsFetcher()
        tweet_formatter = TweetFormatter()
        tweet_poster = TweetPoster()
        
        # Use the new random article posting method
        logger.info("Posting random article from Reuters or MIT Technology Review...")
        news_fetcher.post_random_article()
        logger.info("AI News Tweeter process completed")
        
    except Exception as e:
        logger.error(f"Critical error in main process: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()