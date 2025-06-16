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
    level=logging.INFO,
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
        
        # Fetch latest AI news articles
        logger.info("Fetching latest AI news...")
        articles = news_fetcher.fetch_top_articles(limit=2)
        
        if not articles:
            logger.warning("No articles found to tweet")
            return
        
        # Process each article
        for i, article in enumerate(articles, 1):
            try:
                logger.info(f"Processing article {i}: {article['title'][:50]}...")
                
                # Format article into tweet
                tweet_text = tweet_formatter.format_tweet(
                    title=article['title'],
                    url=article['url'],
                    summary=article.get('summary', '')
                )
                
                if not tweet_text:
                    logger.error(f"Failed to format tweet for article {i}")
                    continue
                
                # Post tweet
                success = tweet_poster.post_tweet(tweet_text)
                
                if success:
                    logger.info(f"Successfully posted tweet {i}")
                    # Mark article as posted only after successful tweet
                    news_fetcher.mark_article_as_posted(article['url'])
                else:
                    logger.error(f"Failed to post tweet {i}")
                    # Don't mark as posted if tweet failed, so it can be retried later
                    
            except Exception as e:
                logger.error(f"Error processing article {i}: {str(e)}")
                continue
        
        logger.info("AI News Tweeter process completed")
        
    except Exception as e:
        logger.error(f"Critical error in main process: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()