#!/usr/bin/env python3
"""
News Fetcher Module
Fetches latest AI/LLM news from various reputable sources
"""

import feedparser
import requests
import logging
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class NewsFetcher:
    """Fetches AI/LLM news from multiple sources"""
    
    def __init__(self):
        self.ai_keywords = [
            'AI', 'artificial intelligence', 'LLM', 'large language model',
            'ChatGPT', 'GPT-4', 'GPT-5', 'Anthropic', 'Claude', 'Transformer',
            'OpenAI', 'machine learning', 'deep learning', 'neural network',
            'Hugging Face', 'Gemini', 'Bard', 'LLaMA', 'Mistral', 'DeepSeek'
        ]
        
        # RSS feeds from reputable AI news sources
        self.rss_feeds = [
            {
                'name': 'The Verge AI',
                'url': 'https://www.theverge.com/ai-artificial-intelligence/rss/index.xml'
            },
            {
                'name': 'TechCrunch AI',
                'url': 'https://techcrunch.com/category/artificial-intelligence/feed/'
            },
            {
                'name': 'MIT Technology Review AI',
                'url': 'https://www.technologyreview.com/topic/artificial-intelligence/feed/'
            },
            {
                'name': 'OpenAI Blog',
                'url': 'https://openai.com/blog/rss.xml'
            },
            {
                'name': 'Hugging Face Blog',
                'url': 'https://huggingface.co/blog/feed.xml'
            },
            {
                'name': 'Anthropic News',
                'url': 'https://www.anthropic.com/news/rss.xml'
            }
        ]
        
        # Load posted articles to avoid duplicates
        self.posted_articles_file = 'posted_articles.json'
        self.posted_articles = self._load_posted_articles()
    
    def _load_posted_articles(self) -> set:
        """Load previously posted article URLs"""
        try:
            if os.path.exists(self.posted_articles_file):
                with open(self.posted_articles_file, 'r') as f:
                    data = json.load(f)
                    return set(data.get('posted_urls', []))
        except Exception as e:
            logger.warning(f"Could not load posted articles: {e}")
        return set()
    
    def _save_posted_articles(self):
        """Save posted article URLs"""
        try:
            data = {
                'posted_urls': list(self.posted_articles),
                'last_updated': datetime.now().isoformat()
            }
            with open(self.posted_articles_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save posted articles: {e}")
    
    def _is_ai_related(self, title: str, summary: str = '') -> bool:
        """Check if article is AI-related based on keywords"""
        text = f"{title} {summary}".lower()
        return any(keyword.lower() in text for keyword in self.ai_keywords)
    
    def _fetch_from_rss(self, feed_info: Dict) -> List[Dict]:
        """Fetch articles from a single RSS feed"""
        articles = []
        try:
            logger.info(f"Fetching from {feed_info['name']}...")
            feed = feedparser.parse(feed_info['url'])
            
            if feed.bozo:
                logger.warning(f"RSS feed parsing warning for {feed_info['name']}: {feed.bozo_exception}")
            
            for entry in feed.entries[:10]:  # Limit to recent entries
                # Check if article is recent (within last 3 days)
                try:
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date = datetime(*entry.published_parsed[:6])
                        if (datetime.now() - pub_date).days > 3:
                            continue
                except:
                    pass  # If date parsing fails, include the article
                
                title = entry.get('title', '').strip()
                url = entry.get('link', '').strip()
                summary = entry.get('summary', '').strip()
                
                # Skip if already posted
                if url in self.posted_articles:
                    continue
                
                # Check if AI-related
                if self._is_ai_related(title, summary):
                    articles.append({
                        'title': title,
                        'url': url,
                        'summary': summary,
                        'source': feed_info['name'],
                        'published': entry.get('published', '')
                    })
            
        except Exception as e:
            logger.error(f"Error fetching from {feed_info['name']}: {e}")
        
        return articles
    
    def fetch_top_articles(self, limit: int = 2) -> List[Dict]:
        """Fetch top AI articles from all sources"""
        all_articles = []
        
        # Fetch from all RSS feeds
        for feed_info in self.rss_feeds:
            articles = self._fetch_from_rss(feed_info)
            all_articles.extend(articles)
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_articles = []
        for article in all_articles:
            if article['url'] not in seen_urls:
                seen_urls.add(article['url'])
                unique_articles.append(article)
        
        # Sort by relevance (simple scoring based on keyword frequency)
        def score_article(article):
            text = f"{article['title']} {article['summary']}".lower()
            score = sum(text.count(keyword.lower()) for keyword in self.ai_keywords)
            return score
        
        unique_articles.sort(key=score_article, reverse=True)
        
        # Return top articles up to limit (don't mark as posted yet)
        top_articles = unique_articles[:limit]
        
        logger.info(f"Found {len(top_articles)} articles to tweet")
        return top_articles
    
    def mark_article_as_posted(self, article_url: str):
        """Mark a specific article as posted after successful tweet"""
        self.posted_articles.add(article_url)
        self._save_posted_articles()
        logger.info(f"Marked article as posted: {article_url}")