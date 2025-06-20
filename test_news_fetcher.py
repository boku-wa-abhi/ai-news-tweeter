#!/usr/bin/env python3
"""Test script for the simplified NewsFetcher class"""

from news_fetcher import NewsFetcher
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_news_fetcher():
    """Test the NewsFetcher functionality"""
    try:
        # Initialize NewsFetcher
        nf = NewsFetcher()
        print("✓ NewsFetcher initialized successfully")
        
        # Test Reuters fetching
        print("\nTesting Reuters Technology news fetching...")
        reuters_articles = nf.fetch_latest_reuters_tech_news()
        print(f"✓ Found {len(reuters_articles)} Reuters articles")
        
        if reuters_articles:
            print("Sample Reuters article:")
            article = reuters_articles[0]
            print(f"  Title: {article['title'][:100]}...")
            print(f"  URL: {article['url'][:100]}...")
            print(f"  Source: {article['source']}")
        
        # Test MIT Tech Review fetching
        print("\nTesting MIT Technology Review article fetching...")
        mit_articles = nf.fetch_latest_mit_tech_review_article()
        print(f"✓ Found {len(mit_articles)} MIT articles")
        
        if mit_articles:
            print("Sample MIT article:")
            article = mit_articles[0]
            print(f"  Title: {article['title'][:100]}...")
            print(f"  URL: {article['url'][:100]}...")
            print(f"  Source: {article['source']}")
        
        # Test random article posting
        print("\nTesting random article posting...")
        nf.post_random_article()
        print("✓ Random article posting test completed")
        
        print("\n🎉 All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_news_fetcher()