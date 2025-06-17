#!/usr/bin/env python3

import logging
logging.basicConfig(level=logging.DEBUG)

from news_fetcher import NewsFetcher

def test_fetch():
    print("Testing RSS fetch and URL extraction...")
    
    nf = NewsFetcher()
    articles = nf.fetch_top_articles(limit=2)
    
    print(f"Found {len(articles)} articles")
    
    for i, article in enumerate(articles):
        print(f"\nArticle {i+1}:")
        print(f"  Title: {article['title'][:80]}...")
        print(f"  URL: {article['url']}")
        print(f"  URL Length: {len(article['url'])} chars")
        if 'original_url' in article:
            print(f"  Original URL: {article['original_url'][:80]}...")
            print(f"  Original URL Length: {len(article['original_url'])} chars")
        print(f"  Source: {article['source']}")

if __name__ == "__main__":
    test_fetch()