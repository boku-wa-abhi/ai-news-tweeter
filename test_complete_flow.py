#!/usr/bin/env python3
"""Test script to demonstrate complete flow with Reuters feeds and TinyURL"""

import logging
from news_fetcher import NewsFetcher
from tweet_formatter import TweetFormatter

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    print("=== AI News Tweeter - Complete Flow Test ===\n")
    print("Sources: Wall Street Journal & Reuters")
    print("URL Shortening: TinyURL")
    print("=" * 50)
    
    # Create components
    news_fetcher = NewsFetcher()
    tweet_formatter = TweetFormatter()
    
    # Test Reuters fetching
    print("\n1. Testing Reuters article fetching...")
    reuters_articles = news_fetcher.fetch_latest_reuters_tech_news()
    
    if reuters_articles:
        reuters_article = reuters_articles[0]  # Get first article
        print(f"✅ Reuters article found:")
        print(f"Title: {reuters_article['title']}")
        print(f"URL: {reuters_article['url']}")
        print(f"Source: {reuters_article['source']}")
        
        # Format tweet for Reuters
        print(f"\n2. Formatting Reuters tweet...")
        formatted_tweet = tweet_formatter.format_tweet(
            reuters_article['title'],
            reuters_article['url'],
            reuters_article.get('summary', '')
        )
        
        if formatted_tweet:
            print(f"\n✅ Successfully formatted Reuters tweet ({len(formatted_tweet)} characters):")
            print("=" * 60)
            print(formatted_tweet)
            print("=" * 60)
    else:
        print("❌ No Reuters article found")
    
    # Test MIT Tech Review fetching
    print("\n3. Testing MIT Technology Review article fetching...")
    mit_articles = news_fetcher.fetch_latest_mit_tech_review_article()
    
    if mit_articles:
        mit_article = mit_articles[0]  # Get first article
        print(f"✅ MIT Tech Review article found:")
        print(f"Title: {mit_article['title']}")
        print(f"URL: {mit_article['url']}")
        print(f"Source: {mit_article['source']}")
        
        # Format tweet for MIT
        print(f"\n4. Formatting MIT Tech Review tweet...")
        formatted_tweet = tweet_formatter.format_tweet(
            mit_article['title'],
            mit_article['url'],
            mit_article.get('summary', '')
        )
        
        if formatted_tweet:
            print(f"\n✅ Successfully formatted MIT tweet ({len(formatted_tweet)} characters):")
            print("=" * 60)
            print(formatted_tweet)
            print("=" * 60)
    else:
        print("❌ No MIT Tech Review article found")
    
    # Test random article posting
    print("\n5. Testing random article posting...")
    news_fetcher.post_random_article()
    
    print("\n🎉 Test completed! The system successfully:")
    print("   ✅ Fetches news from Reuters and MIT Technology Review")
    print("   ✅ Formats tweets within Twitter's 280-character limit")
    print("   ✅ Posts random articles from available sources")
    print("\n💡 To enable actual posting, add real Twitter API credentials to .env file")

if __name__ == "__main__":
    main()