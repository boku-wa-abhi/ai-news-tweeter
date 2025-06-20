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
    """Fetches latest tech news from Reuters and MIT Technology Review"""
    
    def __init__(self):
        self.posted_articles = set()
    

    
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
                    
                    if not relative_url or not title:
                        continue
                        
                    # Construct full URL
                    if relative_url.startswith('/'):
                        full_url = page_info['base_url'] + relative_url
                    else:
                        full_url = relative_url
                    
                    # Add all articles without filtering
                    articles.append({
                        'title': title,
                        'url': full_url,
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
    
    def fetch_latest_reuters_tech_news(self) -> List[Dict]:
        """Fetch the latest Reuters Technology news articles."""
        page_info = {
            'name': 'Reuters Technology',
            'url': 'https://www.reuters.com/technology/',
            'base_url': 'https://www.reuters.com'
        }
        logger.info(f"Fetching latest articles from: {page_info['name']}")
        articles = self._scrape_reuters_tech(page_info)
        if not articles:
            logger.warning("No articles found from Reuters Technology")
        return articles

    def fetch_latest_mit_tech_review_article(self) -> List[Dict]:
        """Fetch the latest article from MIT Technology Review."""
        page_info = {
            'name': 'MIT Technology Review',
            'url': 'https://www.technologyreview.com/2025/05/19/1116614/hao-empire-ai-openai/',
            'base_url': 'https://www.technologyreview.com'
        }
        logger.info(f"Fetching latest article from: {page_info['name']}")
        articles = []
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(page_info['url'], headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('title').get_text().strip()
            if title:
                articles.append({
                    'title': title,
                    'url': page_info['url'],
                    'original_url': page_info['url'],
                    'summary': '',
                    'source': page_info['name'],
                    'published': datetime.now().isoformat()
                })
        except Exception as e:
            logger.error(f"Error fetching from {page_info['name']}: {e}")
        return articles

    def post_random_article(self):
        """Post one of the two articles randomly."""
        import random
        articles = []
        if random.choice([True, False]):
            articles = self.fetch_latest_reuters_tech_news()
        else:
            articles = self.fetch_latest_mit_tech_review_article()
        if articles:
            article = random.choice(articles)
            # Logic to post the article
            logger.info(f"Posting article: {article['title']} from {article['source']}")

    def fetch_top_articles(self, limit: int = 2) -> List[Dict]:
        """Deprecated method - use post_random_article instead"""
        return []
    
    def mark_article_as_posted(self, article_url: str):
        """Mark a specific article as posted after successful tweet"""
        self.posted_articles.add(article_url)
        logger.info(f"Marked article as posted: {article_url}")