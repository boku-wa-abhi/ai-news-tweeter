import os
import random
import logging
from typing import Dict, Any
from news_fetcher import NewsFetcher
from tweet_poster import TweetPoster
from openai import OpenAI

class ViralTweetGenerator:
    def __init__(self):
        self.news_fetcher = NewsFetcher()
        self.tweet_poster = TweetPoster()
        
        # Initialize DeepSeek client
        self.deepseek_client = OpenAI(
            api_key=os.getenv('DEEPSEEK_API_KEY'),
            base_url="https://api.deepseek.com"
        )
        
        # Viral tweet components
        self.hooks = [
            "You won't believe what just dropped in AI today.",
            "This new LLM is changing everything.",
            "Open-source just caught up with GPT-4.",
            "AI devs, you're gonna want this.",
            "This one prompt unlocked my productivity.",
            "Nobody's talking about this AI failure — but they should be.",
            "I built an AI tool in 1 hour. Here's what happened.",
            "This paper blew my mind. 🤯",
            "You've heard of GPT-4, but what's next?",
            "The AI tool stack I wish I had earlier."
        ]
        
        self.value_statements = [
            "Here's a quick summary + how it works.",
            "This could save you hours a week.",
            "Here's the breakdown in 5 lines of code.",
            "You can use it right now. No login.",
            "Here's what makes it better than the rest.",
            "I tested it so you don't have to.",
            "This integrates perfectly with LangChain/DeepSeek.",
            "It's blazing fast and open-source.",
            "Here's how it compares with GPT-4.",
            "Bonus: I built a tiny wrapper to try it out."
        ]
        
        self.emotions = [
            "Surprise", "Empowerment", "Curiosity", "FOMO (fear of missing out)",
            "Inspiration", "Awe", "Humor", "Fear (in moderation)", "Confidence", "Nostalgia"
        ]
        
        self.shareability_triggers = [
            "Tag a dev who needs this.",
            "Retweet so more people can use this.",
            "Save this for later.",
            "DM me if you want a demo.",
            "This will change how you code.",
            "Thread → let's break it down.",
            "Bookmark this thread.",
            "The community needs to see this.",
            "Use this before it gets popular.",
            "I'll open-source this if this gets 50 RTs."
        ]
    
    def generate_viral_tweet(self) -> bool:
        """Generate and post a viral AI tweet"""
        try:
            # Fetch latest AI news
            articles = self.news_fetcher.fetch_latest_newsapi_articles()
            if not articles:
                logging.error("No articles found for viral tweet generation")
                return False
            
            article = articles[0]  # Use the first article
            
            # Randomly select components
            hook = random.choice(self.hooks)
            value = random.choice(self.value_statements)
            emotion = random.choice(self.emotions)
            cta = random.choice(self.shareability_triggers)
            
            # Create prompt for DeepSeek
            prompt = f"""You're an expert viral content creator. Use the following structure to create a viral tweet about this AI news:
HOOK: {hook}
VALUE: {value}
EMOTION: {emotion}
CTA: {cta}

Here is the news: '{article['title']}' — '{article['description']}'. 
Create a tweet under 280 characters with this tone and style. Include emojis only if they help enhance clarity or energy."""
            
            # Generate tweet with DeepSeek
            response = self.deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.8
            )
            
            tweet_content = response.choices[0].message.content.strip()
            
            # Verify character count
            if len(tweet_content) > 280:
                logging.warning(f"Tweet too long ({len(tweet_content)} chars), truncating")
                tweet_content = tweet_content[:277] + "..."
            
            # Post the tweet
            success = self.tweet_poster.post_tweet(tweet_content)
            
            if success:
                logging.info(f"Viral tweet posted successfully: {tweet_content[:50]}...")
                return True
            else:
                logging.error("Failed to post viral tweet")
                return False
                
        except Exception as e:
            logging.error(f"Error generating viral tweet: {str(e)}")
            return False

def main():
    """Main function to generate and post viral tweet"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    generator = ViralTweetGenerator()
    success = generator.generate_viral_tweet()
    
    if success:
        logging.info("Viral tweet generation completed successfully")
    else:
        logging.error("Viral tweet generation failed")
        exit(1)

if __name__ == "__main__":
    main()