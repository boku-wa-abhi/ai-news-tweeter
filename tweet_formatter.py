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
Create a compelling Twitter summary of this AI/tech news in 1-2 complete sentences. 
Make it engaging and informative. Do not use quotes, markdown, or any formatting. 
Just provide clean, readable text that captures the key innovation or development.

Title: {title}
Summary: {summary[:500]}

Write only the summary text without quotes or formatting:"""
            
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
                    # Clean up the summary by removing quotes and extra formatting
                    summary_text = self._clean_summary(summary_text)
                    logger.info("Successfully generated summary using DeepSeek API")
                    return summary_text
            else:
                logger.error(f"DeepSeek API error: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"Error calling DeepSeek API: {e}")
        
        # Fallback to simple summarization
        return self._fallback_summarize(title, summary)
    
    def _clean_summary(self, summary_text: str) -> str:
        """Clean up AI-generated summary by removing unwanted formatting"""
        if not summary_text:
            return summary_text
        
        # Remove leading and trailing whitespace
        summary_text = summary_text.strip()
        
        # Remove leading quotes (both single and double)
        while summary_text and (summary_text.startswith('"') or summary_text.startswith("'")):
            summary_text = summary_text[1:].strip()
        
        # Remove trailing quotes (both single and double)
        while summary_text and (summary_text.endswith('"') or summary_text.endswith("'")):
            summary_text = summary_text[:-1].strip()
        
        # Remove any markdown formatting that might have been added
        summary_text = re.sub(r'^\*\*|\*\*$', '', summary_text)  # Remove bold markdown
        summary_text = re.sub(r'^\*|\*$', '', summary_text)      # Remove italic markdown
        
        return summary_text.strip()
    
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
            
            # Calculate available space for summary with more conservative approach
            # Twitter limit: 280 characters
            # Reserve space for: hashtags + URL + spaces and newlines + buffer
            reserved_space = len(hashtag_text) + len(short_url) + 6  # 6 for spaces, newlines, and buffer
            available_space = 280 - reserved_space
            
            # Ensure we have enough space for a meaningful summary
            if available_space < 50:
                # Reduce hashtags if space is too tight
                hashtags = hashtags[:2]
                hashtag_text = ' '.join(hashtags)
                reserved_space = len(hashtag_text) + len(short_url) + 6
                available_space = 280 - reserved_space
            
            # Smart truncation to ensure complete sentences
            if len(ai_summary) > available_space:
                # First, try to find a good sentence break
                target_length = available_space - 10  # Leave some buffer
                
                # Find sentence boundaries within reasonable range
                sentence_endings = []
                for i, char in enumerate(ai_summary):
                    if char in '.!?' and i < target_length:
                        sentence_endings.append(i)
                
                if sentence_endings:
                    # Use the last complete sentence that fits
                    last_sentence_end = max(sentence_endings)
                    ai_summary = ai_summary[:last_sentence_end + 1]
                else:
                    # No good sentence break found, truncate at word boundary
                    words = ai_summary[:target_length].split()
                    if len(words) > 1:
                        # Remove the last word which might be incomplete
                        ai_summary = ' '.join(words[:-1])
                        # Add proper ending
                        if not ai_summary.endswith(('.', '!', '?')):
                            ai_summary += '.'
                    else:
                        ai_summary = ai_summary[:target_length] + '.'
            
            # Format final tweet
            tweet = f"{ai_summary}\n\n{hashtag_text}\n{short_url}"
            
            # Final safety check
            if len(tweet) > 280:
                logger.warning(f"Tweet still too long ({len(tweet)} chars), applying final truncation...")
                # Calculate exact excess and remove from summary
                excess = len(tweet) - 280
                if len(ai_summary) > excess + 5:
                    # Truncate summary and ensure it ends properly
                    new_summary = ai_summary[:-(excess + 5)]
                    if not new_summary.endswith(('.', '!', '?')):
                        new_summary += '.'
                    ai_summary = new_summary
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