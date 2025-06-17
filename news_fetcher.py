#!/usr/bin/env python3
"""News Fetcher Module
Fetches latest tech news from WSJ and Reuters by scraping their tech pages directly"""

import requests
import logging
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re
import feedparser

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
        
        # Tech RSS feeds (fallback approach since direct scraping may be blocked)
        self.tech_feeds = [
            {
                'name': 'WSJ Technology',
                'url': 'https://feeds.a.dj.com/rss/RSSWSJD.xml',
                'base_url': 'https://www.wsj.com'
            },
            {
                'name': 'Reuters Technology', 
                'url': 'https://www.reuters.com/technology/',
                'base_url': 'https://www.reuters.com'
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
    
    def _is_ai_related(self, title: str, summary: str = "") -> bool:
        """Check if article is AI/tech-related based on keywords"""
        text_to_check = f"{title} {summary}".lower()
        return any(keyword in text_to_check for keyword in self.ai_keywords)
    
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
    
    def _scrape_reuters_tech(self, page_info: Dict) -> List[Dict]:
        """Scrape articles from Reuters technology page"""
        articles = []
        try:
            logger.info(f"Scraping from {page_info['name']}...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(page_info['url'], headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find article links on Reuters tech page
            article_links = soup.find_all('a', {'data-testid': 'Heading'})
            
            for link in article_links[:5]:  # Limit to top 5 articles
                try:
                    title = link.get_text().strip()
                    relative_url = link.get('href', '')
                    
                    if not relative_url:
                        continue
                        
                    # Construct full URL
                    if relative_url.startswith('/'):
                        full_url = page_info['base_url'] + relative_url
                    else:
                        full_url = relative_url
                    
                    # Skip if already posted
                    if full_url in self.posted_articles:
                        continue
                    
                    # Shorten URL using TinyURL
                    short_url = self._shorten_url_with_tinyurl(full_url)
                    
                    # Skip if shortened URL already posted
                    if short_url in self.posted_articles:
                        continue
                    
                    # Check if tech/AI-related
                    if self._is_ai_related(title):
                        articles.append({
                            'title': title,
                            'url': short_url,
                            'original_url': full_url,
                            'summary': '',  # Reuters doesn't provide summary on listing page
                            'source': page_info['name'],
                            'published': datetime.now().isoformat()
                        })
                        
                except Exception as e:
                    logger.warning(f"Error processing Reuters article: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping from {page_info['name']}: {e}")
        
        return articles
    
    def _scrape_wsj_tech(self, page_info: Dict) -> List[Dict]:
        """Scrape articles from WSJ technology page"""
        articles = []
        try:
            logger.info(f"Scraping from {page_info['name']}...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(page_info['url'], headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find article links on WSJ tech page
            article_links = soup.find_all('a', class_=re.compile(r'.*headline.*|.*title.*'))
            
            for link in article_links[:5]:  # Limit to top 5 articles
                try:
                    title = link.get_text().strip()
                    relative_url = link.get('href', '')
                    
                    if not relative_url or not title:
                        continue
                        
                    # Construct full URL
                    if relative_url.startswith('/'):
                        full_url = page_info['base_url'] + relative_url
                    else:
                        full_url = relative_url
                    
                    # Skip if already posted
                    if full_url in self.posted_articles:
                        continue
                    
                    # Shorten URL using TinyURL
                    short_url = self._shorten_url_with_tinyurl(full_url)
                    
                    # Skip if shortened URL already posted
                    if short_url in self.posted_articles:
                        continue
                    
                    # Check if tech/AI-related
                    if self._is_ai_related(title):
                        articles.append({
                            'title': title,
                            'url': short_url,
                            'original_url': full_url,
                            'summary': '',  # WSJ doesn't provide summary on listing page
                            'source': page_info['name'],
                            'published': datetime.now().isoformat()
                        })
                        
                except Exception as e:
                    logger.warning(f"Error processing WSJ article: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping from {page_info['name']}: {e}")
        
        return articles
    
    def _fetch_from_rss(self, feed_info: Dict) -> List[Dict]:
        """Fetch articles from RSS feed"""
        articles = []
        try:
            logger.info(f"Fetching from {feed_info['name']} RSS...")
            feed = feedparser.parse(feed_info['url'])
            
            if feed.bozo:
                logger.warning(f"RSS feed parsing warning for {feed_info['name']}: {feed.bozo_exception}")
            
            for entry in feed.entries[:10]:  # Limit to recent entries
                title = entry.get('title', '').strip()
                original_url = entry.get('link', '').strip()
                summary = entry.get('summary', '').strip()
                
                # Skip if already posted
                if original_url in self.posted_articles:
                    continue
                
                # Shorten URL using TinyURL
                short_url = self._shorten_url_with_tinyurl(original_url)
                
                # Skip if shortened URL already posted
                if short_url in self.posted_articles:
                    continue
                
                # Check if tech/AI-related
                if self._is_ai_related(title, summary):
                    articles.append({
                        'title': title,
                        'url': short_url,
                        'original_url': original_url,
                        'summary': summary,
                        'source': feed_info['name'],
                        'published': entry.get('published', datetime.now().isoformat())
                    })
                    
        except Exception as e:
            logger.error(f"Error fetching from {feed_info['name']} RSS: {e}")
        
        return articles
    
    def fetch_top_articles(self, limit: int = 2) -> List[Dict]:
        """Fetch top tech articles using RSS feeds and web scraping"""
        all_articles = []
        
        # Fetch from tech feeds
        for feed_info in self.tech_feeds:
            if 'reuters' in feed_info['url'].lower():
                # Try scraping Reuters first, fallback to RSS if needed
                articles = self._scrape_reuters_tech(feed_info)
                if not articles:
                    logger.info("Reuters scraping failed, trying RSS fallback...")
                    # Could add RSS fallback here if needed
            elif 'wsj' in feed_info['name'].lower():
                # Use RSS for WSJ since scraping is blocked
                articles = self._fetch_from_rss(feed_info)
            else:
                continue
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