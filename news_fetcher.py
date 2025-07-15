#!/usr/bin/env python3
"""News Fetcher Module
Fetches latest tech news from WSJ and Reuters by scraping their tech pages directly"""

import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import os
from datetime import datetime
import random
from datetime import timedelta
from typing import List, Dict, Optional
import re
import feedparser

logger = logging.getLogger(__name__)

class NewsFetcher:
    """Fetches latest tech news from Reuters and MIT Technology Review"""
    
    def __init__(self):
        self.posted_articles = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # NewsAPI configuration
        self.newsapi_key = os.getenv('NEWSAPI_KEY')
        self.newsapi_url = 'https://newsapi.org/v2/everything'
        
        # TinyURL configuration
        self.tinyurl_api_key = os.getenv('TINYURL_API_KEY')
        self.tinyurl_url = 'https://api.tinyurl.com/create'
        
        # AI-related keywords for NewsAPI search
        self.ai_keywords = [
            # Core AI & ML Terms
            'Artificial Intelligence', 'Machine Learning', 'Deep Learning', 'Neural Networks',
            'Transformers', 'LSTM', 'Attention Mechanism', 'Reinforcement Learning',
            'Self-Supervised Learning', 'Generative Models',
            
            # Large Language Models (LLMs)
            'Large Language Model', 'LLM', 'GPT', 'GPT-4', 'GPT-5', 'OpenAI',
            'ChatGPT', 'Claude', 'LLaMA', 'Mistral',
            
            # Natural Language Processing (NLP)
            'Natural Language Processing', 'Language Model', 'Prompt Engineering',
            'Tokenization', 'Fine-Tuning', 'Embeddings', 'Zero-shot Learning',
            'Few-shot Learning', 'In-context Learning', 'Prompt Tuning',
            
            # AI Tools & Libraries
            'Hugging Face', 'LangChain', 'Transformers Library', 'PyTorch',
            'TensorFlow', 'Open Source LLM', 'AutoGPT', 'DeepSeek', 'Ollama', 'FastChat',
            
            # Autonomous Agents & Tools
            'Autonomous Agents', 'ReAct', 'Toolformer', 'BabyAGI', 'AutoGPT',
            'Agentic Workflow', 'LLM Agents', 'AI Agent', 'LangGraph', 'Memory-Augmented Agents',
            
            # Conversational AI
            'Chatbot', 'Conversational AI', 'Dialogue Systems', 'Retrieval-Augmented Generation',
            'RAG', 'Vector Database', 'Pinecone', 'FAISS', 'Milvus', 'Semantic Search',
            
            # AI Research & Models
            'Paper with Code', 'Arxiv', 'Google DeepMind', 'Meta AI', 'Anthropic',
            'Perplexity', 'Mamba Model', 'RWKV', 'Gemini AI', 'PaLM',
            
            # Applications
            'Text-to-Image', 'Text-to-Video', 'Image Generation', 'Code Generation',
            'AI Coding Assistant', 'AI Content Creation', 'AI Research Tools',
            'Document AI', 'LLM for Business', 'Chat with PDF',
            
            # Trends & Ecosystem
            'AI Safety', 'Hallucination', 'Red Teaming', 'Prompt Injection',
            'Alignment', 'Model Compression', 'Quantization', 'LoRA', 'PEFT', 'AI Regulation',
            
            # Industry Buzz & Companies
            'NVIDIA', 'OpenAI Dev Day', 'AGI', 'AI Startup', 'AI Funding',
            'AI Scaling Laws', 'AI Ethics', 'VC in AI', 'Open Weight Models', 'AI Future'
        ]
    

    
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
    


    def fetch_latest_newsapi_articles(self) -> List[Dict]:
        """Fetch latest AI news from NewsAPI using random keywords"""
        articles = []
        
        if not self.newsapi_key:
            logger.warning("NewsAPI key not available")
            return articles
        
        try:
            # Randomly select a keyword
            keyword = random.choice(self.ai_keywords)
            logger.info(f"Searching NewsAPI for keyword: {keyword}")
            
            # NewsAPI parameters
            params = {
                'q': keyword,
                'apiKey': self.newsapi_key,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 5,  # Get top 5 articles
                'domains': 'techcrunch.com,wired.com,arstechnica.com,theverge.com,venturebeat.com,zdnet.com,engadget.com,mashable.com,thenextweb.com,ieee.org'
            }
            
            response = self.session.get(self.newsapi_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 'ok' and data.get('articles'):
                for article_data in data['articles']:
                    if article_data.get('title') and article_data.get('url'):
                        # Skip articles with [Removed] content
                        if '[Removed]' in str(article_data.get('title', '')) or '[Removed]' in str(article_data.get('description', '')):
                            continue
                            
                        original_url = article_data.get('url', '')
                        shortened_url = self._shorten_url_with_tinyurl(original_url)
                        
                        article = {
                            'title': article_data['title'],
                            'url': shortened_url,
                            'original_url': original_url,
                            'summary': article_data.get('description', ''),
                            'source': f"NewsAPI ({keyword})",
                            'published_at': article_data.get('publishedAt', ''),
                            'keyword': keyword
                        }
                        articles.append(article)
                        
                logger.info(f"Found {len(articles)} articles from NewsAPI for keyword: {keyword}")
            else:
                logger.warning(f"No articles found from NewsAPI for keyword: {keyword}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching from NewsAPI: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in NewsAPI fetch: {e}")
            
        return articles

    def post_random_article(self) -> bool:
        """Post a random article from NewsAPI"""
        try:
            from tweet_formatter import TweetFormatter
            from tweet_poster import TweetPoster
            
            logger.info("Fetching latest articles from: NewsAPI")
            articles = self.fetch_latest_newsapi_articles()
            
            if not articles:
                logger.warning("No articles found from NewsAPI")
                return False
            
            # Select the first article
            article = articles[0]
            logger.info(f"Selected article for posting: {article.get('title', 'Unknown title')}")
            
            # Format the tweet
            tweet_formatter = TweetFormatter()
            tweet_text = tweet_formatter.format_tweet(
                title=article.get('title', ''),
                url=article.get('url', ''),
                summary=article.get('summary', '')
            )
            
            if not tweet_text:
                logger.error(f"Failed to format tweet for: {article.get('title', 'Unknown title')}")
                return False
            
            # Post the tweet
            tweet_poster = TweetPoster()
            success = tweet_poster.post_tweet(tweet_text)
            
            if success:
                logger.info(f"Successfully posted tweet for: {article.get('title', 'Unknown title')}")
                return True
            else:
                logger.error(f"Failed to post tweet for: {article.get('title', 'Unknown title')}")
                return False
                
        except Exception as e:
            logger.error(f"Error in post_random_article: {e}")
            return False

    def fetch_top_articles(self, limit: int = 2) -> List[Dict]:
        """Deprecated method - use post_random_article instead"""
        return []
    
    def mark_article_as_posted(self, article_url: str):
        """Mark a specific article as posted after successful tweet"""
        self.posted_articles.add(article_url)
        logger.info(f"Marked article as posted: {article_url}")