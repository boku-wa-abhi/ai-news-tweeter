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
        
        # Fetch latest tech news articles from WSJ and Reuters
        logger.info("Fetching latest tech news from WSJ and Reuters...")
        articles = news_fetcher.fetch_top_articles(limit=10)  # Get more articles to find the latest one
        
        if not articles:
            logger.warning("No articles found to tweet")
            return
        
        # Sort articles by published date to get the latest one
        articles.sort(key=lambda x: x.get('published', ''), reverse=True)
        latest_article = articles[0]
        
        logger.info(f"Selected latest article: {latest_article['title'][:50]}...")
        logger.info(f"Article URL length: {len(latest_article['url'])} chars")
        logger.info(f"Source: {latest_article['source']}")
        
        # Format article into tweet
        tweet_text = tweet_formatter.format_tweet(
            title=latest_article['title'],
            url=latest_article['url'],
            summary=latest_article.get('summary', '')
        )
        
        if not tweet_text:
            logger.error("Failed to format tweet for the latest article")
            return
        
        # Post tweet
        success = tweet_poster.post_tweet(tweet_text)
        
        if success:
            logger.info("Successfully posted tweet for the latest article")
            # Mark article as posted only after successful tweet
            news_fetcher.mark_article_as_posted(latest_article['url'])
            # Update rotation state after successful posting
            news_fetcher._update_rotation_state()
        else:
            logger.error("Failed to post tweet for the latest article")
            return
        
        logger.info("AI News Tweeter process completed")
        
    except Exception as e:
        logger.error(f"Critical error in main process: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()