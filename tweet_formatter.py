#!/usr/bin/env python3
"""
Tweet Formatter Module
Summarizes articles using DeepSeek API and formats them into tweetable posts
"""

import os
import requests
import logging
import re
from typing import Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class TweetFormatter:
    """Formats articles into tweets using DeepSeek API for summarization"""
    
    def __init__(self):
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        if not self.deepseek_api_key:
            logger.warning("DEEPSEEK_API_KEY not found in environment variables")
        
        self.deepseek_api_url = "https://api.deepseek.com/v1/chat/completions"
        
        # Common AI hashtags
        self.ai_hashtags = [
            '#AI', '#ArtificialIntelligence', '#MachineLearning', '#DeepLearning',
            '#LLM', '#ChatGPT', '#OpenAI', '#TechNews', '#Innovation'
        ]
    
    def _get_relevant_hashtags(self, title: str, summary: str) -> list:
        """Get relevant hashtags based on article content"""
        text = f"{title} {summary}".lower()
        relevant_tags = []
        
        # Add specific hashtags based on content
        if any(term in text for term in ['chatgpt', 'gpt-4', 'gpt-5']):
            relevant_tags.append('#ChatGPT')
        if any(term in text for term in ['openai']):
            relevant_tags.append('#OpenAI')
        if any(term in text for term in ['anthropic', 'claude']):
            relevant_tags.append('#Anthropic')
        if any(term in text for term in ['google', 'gemini', 'bard']):
            relevant_tags.append('#Google')
        if any(term in text for term in ['llm', 'large language model']):
            relevant_tags.append('#LLM')
        if any(term in text for term in ['machine learning', 'ml']):
            relevant_tags.append('#MachineLearning')
        
        # Always include basic AI tags
        if '#AI' not in relevant_tags:
            relevant_tags.append('#AI')
        if '#TechNews' not in relevant_tags:
            relevant_tags.append('#TechNews')
        
        return relevant_tags[:3]  # Limit to 3 hashtags
    
    def _shorten_url(self, url: str) -> str:
        """Simple URL shortening (in practice, you might use bit.ly or similar)"""
        # For now, just return the original URL
        # In production, you might want to integrate with URL shortening services
        return url
    
    def _summarize_with_deepseek(self, title: str, summary: str) -> Optional[str]:
        """Summarize article using DeepSeek API"""
        if not self.deepseek_api_key:
            logger.warning("DeepSeek API key not available, using fallback summarization")
            return self._fallback_summarize(title, summary)
        
        try:
            headers = {
                'Authorization': f'Bearer {self.deepseek_api_key}',
                'Content-Type': 'application/json'
            }
            
            prompt = f"""
Summarize this AI/tech news article in 1-2 engaging sentences suitable for Twitter. 
Focus on the key innovation or development. Keep it concise and interesting.

Title: {title}
Summary: {summary[:500]}  # Limit summary length

Provide only the summary, no additional text:"""
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 100,
                "temperature": 0.7
            }
            
            response = requests.post(
                self.deepseek_api_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    summary_text = result['choices'][0]['message']['content'].strip()
                    logger.info("Successfully generated summary using DeepSeek API")
                    return summary_text
            else:
                logger.error(f"DeepSeek API error: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"Error calling DeepSeek API: {e}")
        
        # Fallback to simple summarization
        return self._fallback_summarize(title, summary)
    
    def _fallback_summarize(self, title: str, summary: str) -> str:
        """Fallback summarization when API is not available"""
        # Simple extraction of first sentence or key points
        if summary:
            # Get first sentence
            sentences = re.split(r'[.!?]+', summary)
            if sentences and len(sentences[0]) > 20:
                return sentences[0].strip() + '.'
        
        # If no good summary, use title with some enhancement
        return f"Breaking: {title}"
    
    def format_tweet(self, title: str, url: str, summary: str = '') -> Optional[str]:
        """Format article into a tweet"""
        try:
            # Get AI-generated summary
            ai_summary = self._summarize_with_deepseek(title, summary)
            if not ai_summary:
                logger.error("Failed to generate summary")
                return None
            
            # Get relevant hashtags
            hashtags = self._get_relevant_hashtags(title, summary)
            hashtag_text = ' '.join(hashtags)
            
            # Shorten URL if needed
            short_url = self._shorten_url(url)
            
            # Calculate available space for summary
            # Twitter limit: 280 characters
            # Reserve space for: hashtags + URL + spaces
            reserved_space = len(hashtag_text) + len(short_url) + 4  # 4 for spaces and newlines
            available_space = 280 - reserved_space
            
            # Truncate summary if needed
            if len(ai_summary) > available_space:
                ai_summary = ai_summary[:available_space-3] + '...'
            
            # Format final tweet
            tweet = f"{ai_summary}\n\n{hashtag_text}\n{short_url}"
            
            # Verify tweet length
            if len(tweet) > 280:
                logger.warning(f"Tweet too long ({len(tweet)} chars), truncating...")
                # Emergency truncation
                excess = len(tweet) - 280
                ai_summary = ai_summary[:-excess-3] + '...'
                tweet = f"{ai_summary}\n\n{hashtag_text}\n{short_url}"
            
            logger.info(f"Formatted tweet ({len(tweet)} chars): {tweet[:50]}...")
            return tweet
            
        except Exception as e:
            logger.error(f"Error formatting tweet: {e}")
            return None
    
    def validate_tweet(self, tweet: str) -> bool:
        """Validate tweet format and length"""
        if not tweet:
            return False
        
        if len(tweet) > 280:
            logger.error(f"Tweet too long: {len(tweet)} characters")
            return False
        
        # Check if tweet contains URL
        if 'http' not in tweet:
            logger.warning("Tweet doesn't contain URL")
            return False
        
        return True