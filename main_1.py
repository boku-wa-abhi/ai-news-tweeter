#!/usr/bin/env python3
"""
Main orchestrator for AI News Tweeter with Viral Tweet Generation
Fetches AI news, formats tweets, posts them to Twitter, and generates viral tweets
"""

import os
import sys
import logging
from datetime import datetime

from news_fetcher import NewsFetcher
from tweet_formatter import TweetFormatter
from tweet_poster import TweetPoster
from viral_tweet_generator import ViralTweetGenerator

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
    """Main function to orchestrate both news tweeting and viral tweet generation"""
    try:
        logger.info("Starting AI News Tweeter with Viral Tweet Generation process")
        
        # Initialize components
        news_fetcher = NewsFetcher()
        tweet_formatter = TweetFormatter()
        tweet_poster = TweetPoster()
        viral_generator = ViralTweetGenerator()
        
        # Post article from NewsAPI
        logger.info("Posting article from NewsAPI...")
        news_success = news_fetcher.post_random_article()
        
        if news_success:
            logger.info("Successfully posted AI news tweet")
        else:
            logger.error("Failed to post AI news tweet")
        
        # Generate and post viral tweet
        logger.info("Generating and posting viral tweet...")
        viral_success = viral_generator.generate_viral_tweet()
        
        if viral_success:
            logger.info("Successfully posted viral tweet")
        else:
            logger.error("Failed to post viral tweet")
        
        # Summary
        if news_success and viral_success:
            logger.info("Both news tweet and viral tweet posted successfully")
        elif news_success or viral_success:
            logger.warning("Only one tweet type posted successfully")
        else:
            logger.error("Both tweet types failed to post")
            
        logger.info("AI News Tweeter with Viral Tweet Generation process completed")
        
    except Exception as e:
        logger.error(f"Critical error in main process: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()