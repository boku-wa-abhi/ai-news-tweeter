#!/usr/bin/env python3
"""
Tweet Poster Module
Posts formatted tweets to Twitter using the Twitter API
"""

import os
import tweepy
import logging
import json
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

class TweetPoster:
    """Posts tweets to Twitter using the Twitter API"""
    
    def __init__(self):
        # Get Twitter API credentials from environment variables
        self.consumer_key = os.getenv('TWITTER_API_KEY') or os.getenv('TWITTER_CONSUMER_KEY')
        self.consumer_secret = os.getenv('TWITTER_API_SECRET') or os.getenv('TWITTER_CONSUMER_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET') or os.getenv('TWITTER_ACCESS_SECRET')
        
        # Validate credentials
        self.credentials_valid = all([
            self.consumer_key,
            self.consumer_secret,
            self.access_token,
            self.access_token_secret
        ])
        
        if not self.credentials_valid:
            logger.error("Twitter API credentials not found in environment variables")
            logger.error("Required: TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET")
        
        self.api = None
        self.client = None
        self._initialize_twitter_api()
        
        # File to log posted tweets
        self.tweet_log_file = 'posted_tweets.json'
    
    def _initialize_twitter_api(self):
        """Initialize Twitter API clients"""
        if not self.credentials_valid:
            return
        
        try:
            # Initialize API v1.1 (for legacy support)
            auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            auth.set_access_token(self.access_token, self.access_token_secret)
            self.api = tweepy.API(auth, wait_on_rate_limit=True)
            
            # Initialize API v2 (recommended for new features)
            self.client = tweepy.Client(
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                wait_on_rate_limit=True
            )
            
            # Test authentication
            self._test_authentication()
            
        except Exception as e:
            logger.error(f"Failed to initialize Twitter API: {e}")
            self.api = None
            self.client = None
    
    def _test_authentication(self):
        """Test Twitter API authentication"""
        try:
            if self.client:
                user = self.client.get_me()
                logger.info(f"Twitter API authenticated successfully for user: @{user.data.username}")
            elif self.api:
                user = self.api.verify_credentials()
                logger.info(f"Twitter API authenticated successfully for user: @{user.screen_name}")
        except Exception as e:
            logger.error(f"Twitter API authentication failed: {e}")
            raise
    
    def _log_posted_tweet(self, tweet_text: str, tweet_id: Optional[str] = None):
        """Log posted tweet to file"""
        try:
            # Load existing log
            tweet_log = []
            if os.path.exists(self.tweet_log_file):
                with open(self.tweet_log_file, 'r') as f:
                    tweet_log = json.load(f)
            
            # Add new tweet
            tweet_entry = {
                'timestamp': datetime.now().isoformat(),
                'tweet_text': tweet_text,
                'tweet_id': tweet_id,
                'character_count': len(tweet_text)
            }
            tweet_log.append(tweet_entry)
            
            # Keep only last 100 tweets
            tweet_log = tweet_log[-100:]
            
            # Save updated log
            with open(self.tweet_log_file, 'w') as f:
                json.dump(tweet_log, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to log posted tweet: {e}")
    
    def post_tweet(self, tweet_text: str) -> bool:
        """Post a tweet to Twitter"""
        if not self.credentials_valid:
            logger.error("Cannot post tweet: Twitter API credentials not available")
            return False
        
        if not self.client and not self.api:
            logger.error("Cannot post tweet: Twitter API not initialized")
            return False
        
        # Validate tweet
        if not tweet_text or len(tweet_text.strip()) == 0:
            logger.error("Cannot post empty tweet")
            return False
        
        if len(tweet_text) > 280:
            logger.error(f"Tweet too long: {len(tweet_text)} characters")
            return False
        
        try:
            # Try posting with API v2 first
            if self.client:
                response = self.client.create_tweet(text=tweet_text)
                tweet_id = response.data['id']
                logger.info(f"Tweet posted successfully with ID: {tweet_id}")
                
            # Fallback to API v1.1
            elif self.api:
                status = self.api.update_status(tweet_text)
                tweet_id = status.id_str
                logger.info(f"Tweet posted successfully with ID: {tweet_id}")
            
            else:
                logger.error("No Twitter API client available")
                return False
            
            # Log the posted tweet
            self._log_posted_tweet(tweet_text, tweet_id)
            
            return True
            
        except tweepy.TooManyRequests:
            logger.error("Twitter API rate limit exceeded")
            return False
            
        except tweepy.Forbidden as e:
            logger.error(f"Twitter API forbidden error: {e}")
            return False
            
        except tweepy.BadRequest as e:
            logger.error(f"Twitter API bad request: {e}")
            return False
            
        except Exception as e:
            logger.error(f"Unexpected error posting tweet: {e}")
            return False
    
    def get_tweet_history(self, limit: int = 10) -> list:
        """Get history of posted tweets"""
        try:
            if os.path.exists(self.tweet_log_file):
                with open(self.tweet_log_file, 'r') as f:
                    tweet_log = json.load(f)
                    return tweet_log[-limit:]
        except Exception as e:
            logger.error(f"Failed to get tweet history: {e}")
        return []
    
    def test_connection(self) -> bool:
        """Test Twitter API connection"""
        try:
            self._test_authentication()
            return True
        except:
            return False