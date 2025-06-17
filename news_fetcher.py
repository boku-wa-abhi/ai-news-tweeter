#!/usr/bin/env python3
"""News Fetcher Module
Fetches latest AI/LLM news from major financial and tech news sources via Google News RSS feeds
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
            'Hugging Face', 'Gemini', 'Bard', 'LLaMA', 'Mistral', 'DeepSeek',
            'automation', 'robotics', 'computer vision', 'natural language processing',
            'NLP', 'generative AI', 'AGI', 'artificial general intelligence',
            'algorithm', 'data science', 'predictive analytics', 'tech innovation',
            'digital transformation', 'AI investment', 'AI startup', 'AI regulation'
        ]
        
        # RSS feeds for AI topics from WSJ and Reuters only
        self.rss_feeds = [
            {
                'name': 'Reuters - AI News',
                'url': 'https://news.google.com/rss/search?q=artificial+intelligence+site:reuters.com&hl=en-US&gl=US&ceid=US:en'
            },
            {
                'name': 'Wall Street Journal - AI News',
                'url': 'https://news.google.com/rss/search?q=artificial+intelligence+site:wsj.com&hl=en-US&gl=US&ceid=US:en'
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
    
    def _shorten_url_with_tinyurl(self, url: str) -> str:
        """Shorten URL using TinyURL authenticated API service"""
        try:
            logger.debug(f"Shortening URL with TinyURL: {url[:100]}...")
            
            # Get TinyURL API key from environment
            api_key = os.getenv('TINYURL_API_KEY')
            if not api_key:
                logger.warning("TinyURL API key not found, falling back to free endpoint")
                # Fallback to free endpoint
                tinyurl_api = "http://tinyurl.com/api-create.php"
                response = requests.get(tinyurl_api, params={'url': url}, timeout=10)
                
                if response.status_code == 200:
                    short_url = response.text.strip()
                    if short_url.startswith('http'):
                        logger.info(f"Successfully shortened URL (free): {short_url} (length: {len(short_url)})")
                        return short_url
                return url
            
            # Use authenticated TinyURL API
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            params = {
                'api_token': api_key
            }
            
            json_data = {
                'url': url,
                'domain': 'tinyurl.com'  # Use default domain
            }
            
            response = requests.post(
                'https://api.tinyurl.com/create',
                params=params,
                headers=headers,
                json=json_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'data' in result and 'tiny_url' in result['data']:
                    short_url = result['data']['tiny_url']
                    logger.info(f"Successfully shortened URL: {short_url} (length: {len(short_url)})")
                    return short_url
                else:
                    logger.warning(f"TinyURL API returned unexpected response: {result}")
            else:
                logger.warning(f"TinyURL API returned status code: {response.status_code}")
                
        except requests.RequestException as e:
            logger.warning(f"Failed to shorten URL with TinyURL: {e}")
        except Exception as e:
            logger.warning(f"Error during URL shortening: {e}")
        
        # If shortening fails, return original URL
        logger.debug(f"Using original URL: {url[:100]}...")
        return url
    
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
                original_url = entry.get('link', '').strip()
                summary = entry.get('summary', '').strip()
                
                # Shorten URL using TinyURL
                logger.info(f"Original URL length: {len(original_url)} chars")
                short_url = self._shorten_url_with_tinyurl(original_url)
                logger.info(f"Shortened URL length: {len(short_url)} chars")
                
                # Skip if already posted (check both original and shortened URL)
                if original_url in self.posted_articles or short_url in self.posted_articles:
                    continue
                
                # Check if AI-related
                if self._is_ai_related(title, summary):
                    articles.append({
                        'title': title,
                        'url': short_url,  # Use the shortened URL
                        'original_url': original_url,  # Keep original for reference
                        'summary': summary,
                        'source': feed_info['name'],
                        'published': entry.get('published', '')
                    })
            
        except Exception as e:
            logger.error(f"Error fetching from {feed_info['name']}: {e}")
        
        return articles
    
    def fetch_top_articles(self, limit: int = 2) -> List[Dict]:
        """Fetch top AI articles from Google News across major financial and tech news sources"""
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
        
        # Filter articles by URL length (TinyURL creates short URLs, typically ≤ 30 characters)
        short_url_articles = [article for article in unique_articles if len(article['url']) <= 50]
        long_url_articles = [article for article in unique_articles if len(article['url']) > 50]
        
        # Sort by relevance (simple scoring based on keyword frequency)
        def score_article(article):
            text = f"{article['title']} {article['summary']}".lower()
            score = sum(text.count(keyword.lower()) for keyword in self.ai_keywords)
            return score
        
        short_url_articles.sort(key=score_article, reverse=True)
        long_url_articles.sort(key=score_article, reverse=True)
        
        # Prioritize short URL articles, fallback to long URL articles if needed
        selected_articles = []
        
        # First, try to get articles with short URLs
        if short_url_articles:
            selected_articles.extend(short_url_articles[:limit])
            logger.info(f"Selected {len(selected_articles)} articles with short URLs (≤50 chars)")
        
        # If we need more articles and don't have enough short URL ones, add long URL articles
        if len(selected_articles) < limit and long_url_articles:
            remaining_needed = limit - len(selected_articles)
            selected_articles.extend(long_url_articles[:remaining_needed])
            logger.info(f"Added {min(remaining_needed, len(long_url_articles))} articles with long URLs (>50 chars)")
        
        logger.info(f"Found {len(selected_articles)} articles to tweet")
        return selected_articles
    
    def mark_article_as_posted(self, article_url: str):
        """Mark a specific article as posted after successful tweet"""
        self.posted_articles.add(article_url)
        self._save_posted_articles()
        logger.info(f"Marked article as posted: {article_url}")