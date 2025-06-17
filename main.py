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
        
        # Fetch latest AI news articles (get more to handle URL filtering)
        logger.info("Fetching latest AI news...")
        articles = news_fetcher.fetch_top_articles(limit=5)  # Get more articles to handle filtering
        
        if not articles:
            logger.warning("No articles found to tweet")
            return
        
        # Process articles until we find one that works
        tweet_posted = False
        for article in articles:
            try:
                logger.info(f"Processing article: {article['title'][:50]}...")
                logger.info(f"Article URL length: {len(article['url'])} chars")
                
                # Format article into tweet
                tweet_text = tweet_formatter.format_tweet(
                    title=article['title'],
                    url=article['url'],
                    summary=article.get('summary', '')
                )
                
                if not tweet_text:
                    logger.warning("Failed to format tweet for article (likely URL too long), trying next article...")
                    continue
                
                # Post tweet
                success = tweet_poster.post_tweet(tweet_text)
                
                if success:
                    logger.info("Successfully posted tweet")
                    # Mark article as posted only after successful tweet
                    news_fetcher.mark_article_as_posted(article['url'])
                    tweet_posted = True
                    break
                else:
                    logger.error("Failed to post tweet, trying next article...")
                    continue
                    
            except Exception as e:
                logger.error(f"Error processing article: {str(e)}, trying next article...")
                continue
        
        if not tweet_posted:
            logger.error("Failed to post any tweet from available articles")
            return
        
        logger.info("AI News Tweeter process completed")
        
    except Exception as e:
        logger.error(f"Critical error in main process: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()