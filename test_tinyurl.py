#!/usr/bin/env python3
"""Test script to check TinyURL functionality with Reuters feeds"""

import logging
from news_fetcher import NewsFetcher

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    print("=== Testing Reuters feeds with TinyURL ===\n")
    
    # Create news fetcher
    nf = NewsFetcher()
    
    # Fetch articles
    articles = nf.fetch_top_articles(2)
    
    print(f"\n=== FETCHED {len(articles)} ARTICLES ===\n")
    
    for i, article in enumerate(articles, 1):
        print(f"Article {i}:")
        print(f"  Title: {article['title']}")
        print(f"  Source: {article['source']}")
        print(f"  Original URL: {article['original_url']}")
        print(f"  Original URL Length: {len(article['original_url'])} chars")
        print(f"  Shortened URL: {article['url']}")
        print(f"  Shortened URL Length: {len(article['url'])} chars")
        print(f"  Summary: {article['summary'][:100]}...")
        print("---\n")

if __name__ == "__main__":
    main()