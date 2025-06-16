#!/usr/bin/env python3
"""
Test Setup Script
Verifies that all components are working correctly before deployment
"""

import os
import sys
import logging
from datetime import datetime

# Configure logging for testing
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_environment_variables():
    """Test if all required environment variables are set"""
    logger.info("Testing environment variables...")
    
    required_vars = [
        'DEEPSEEK_API_KEY',
        'TWITTER_CONSUMER_KEY',
        'TWITTER_CONSUMER_SECRET',
        'TWITTER_ACCESS_TOKEN',
        'TWITTER_ACCESS_SECRET'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
        else:
            logger.info(f"✓ {var} is set")
    
    if missing_vars:
        logger.error(f"✗ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    logger.info("✓ All environment variables are set")
    return True

def test_imports():
    """Test if all required modules can be imported"""
    logger.info("Testing module imports...")
    
    try:
        import tweepy
        logger.info("✓ tweepy imported successfully")
    except ImportError as e:
        logger.error(f"✗ Failed to import tweepy: {e}")
        return False
    
    try:
        import feedparser
        logger.info("✓ feedparser imported successfully")
    except ImportError as e:
        logger.error(f"✗ Failed to import feedparser: {e}")
        return False
    
    try:
        import requests
        logger.info("✓ requests imported successfully")
    except ImportError as e:
        logger.error(f"✗ Failed to import requests: {e}")
        return False
    
    # Test our custom modules
    try:
        from news_fetcher import NewsFetcher
        logger.info("✓ news_fetcher imported successfully")
    except ImportError as e:
        logger.error(f"✗ Failed to import news_fetcher: {e}")
        return False
    
    try:
        from tweet_formatter import TweetFormatter
        logger.info("✓ tweet_formatter imported successfully")
    except ImportError as e:
        logger.error(f"✗ Failed to import tweet_formatter: {e}")
        return False
    
    try:
        from tweet_poster import TweetPoster
        logger.info("✓ tweet_poster imported successfully")
    except ImportError as e:
        logger.error(f"✗ Failed to import tweet_poster: {e}")
        return False
    
    logger.info("✓ All modules imported successfully")
    return True

def test_twitter_connection():
    """Test Twitter API connection"""
    logger.info("Testing Twitter API connection...")
    
    try:
        from tweet_poster import TweetPoster
        poster = TweetPoster()
        
        if poster.test_connection():
            logger.info("✓ Twitter API connection successful")
            return True
        else:
            logger.error("✗ Twitter API connection failed")
            return False
    except Exception as e:
        logger.error(f"✗ Twitter API test failed: {e}")
        return False

def test_news_fetching():
    """Test news fetching functionality"""
    logger.info("Testing news fetching...")
    
    try:
        from news_fetcher import NewsFetcher
        fetcher = NewsFetcher()
        
        # Try to fetch one article
        articles = fetcher.fetch_top_articles(limit=1)
        
        if articles:
            logger.info(f"✓ Successfully fetched {len(articles)} article(s)")
            logger.info(f"  Sample article: {articles[0]['title'][:50]}...")
            return True
        else:
            logger.warning("⚠ No articles found (this might be normal)")
            return True  # Not necessarily an error
    except Exception as e:
        logger.error(f"✗ News fetching test failed: {e}")
        return False

def test_tweet_formatting():
    """Test tweet formatting functionality"""
    logger.info("Testing tweet formatting...")
    
    try:
        from tweet_formatter import TweetFormatter
        formatter = TweetFormatter()
        
        # Test with sample data
        sample_title = "OpenAI Releases New GPT-4 Model with Enhanced Capabilities"
        sample_url = "https://example.com/news/gpt4-release"
        sample_summary = "OpenAI has announced the release of an updated GPT-4 model with improved reasoning capabilities and better performance across various tasks."
        
        tweet = formatter.format_tweet(sample_title, sample_url, sample_summary)
        
        if tweet and formatter.validate_tweet(tweet):
            logger.info("✓ Tweet formatting successful")
            logger.info(f"  Sample tweet ({len(tweet)} chars): {tweet[:100]}...")
            return True
        else:
            logger.error("✗ Tweet formatting failed")
            return False
    except Exception as e:
        logger.error(f"✗ Tweet formatting test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("=" * 50)
    logger.info("AI News Tweeter - Setup Test")
    logger.info("=" * 50)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Module Imports", test_imports),
        ("Twitter Connection", test_twitter_connection),
        ("News Fetching", test_news_fetching),
        ("Tweet Formatting", test_tweet_formatting)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("TEST SUMMARY")
    logger.info("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Your setup is ready for deployment.")
        return True
    else:
        logger.error("❌ Some tests failed. Please fix the issues before deploying.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)