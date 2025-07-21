import os
import logging
import random
from typing import Dict, Any
from openai import OpenAI
from tweet_poster import TweetPoster
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ViralTweetGenerator:
    def __init__(self):
        # Initialize DeepSeek client
        deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        if not deepseek_api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable is required")
        
        self.deepseek_client = OpenAI(
            api_key=deepseek_api_key,
            base_url="https://api.deepseek.com"
        )
        
        # Initialize tweet poster (optional for testing)
        try:
            self.tweet_poster = TweetPoster()
            self.can_post = True
        except Exception as e:
            logging.warning(f"Twitter API not configured: {e}")
            self.tweet_poster = None
            self.can_post = False
        
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
        

        
        self.emotions = [
            "Surprise", "Empowerment", "Curiosity", "FOMO (fear of missing out)",
            "Inspiration", "Awe", "Humor", "Fear (in moderation)", "Confidence", "Nostalgia"
        ]
        

    

    
    def generate_viral_tweet(self) -> bool:
        """Generate and post a viral AI tweet"""
        try:
            # Randomly select components
            hook = random.choice(self.hooks)

            emotion = random.choice(self.emotions)

            
            # Log the selected components
            logging.info(f"Selected Hook: {hook}")

            logging.info(f"Selected Emotion: {emotion}")

            
            # Create prompt for DeepSeek
            prompt = f"""You're an expert viral content creator specializing in AI topics. Create a single, cohesive tweet that naturally incorporates:
- Hook: {hook}

- Emotion: {emotion}


Requirements:
- Weave these elements into natural, flowing text without using labels like '**HOOK:**'
- Add 2-3 relevant hashtags at the end
- No markdown formatting (no asterisks, bold, italics)
- Do not mention any specific papers or models without providing their names
- Keep entire tweet under 280 characters
- Make it engaging, informative, and shareable
- Include emojis only if they enhance clarity or energy
- Do not include any call to action"""
            
            # Generate tweet with DeepSeek
            response = self.deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.8
            )
            
            generated_tweet = response.choices[0].message.content.strip()
            
            # Ensure tweet is under 280 characters
            if len(generated_tweet) > 280:
                # Truncate the generated content to fit character limit
                final_tweet = generated_tweet[:280].rsplit(' ', 1)[0]
                logging.warning(f"Tweet truncated to fit character limit: {len(final_tweet)} chars")
            else:
                final_tweet = generated_tweet
            
            # Post the tweet if Twitter API is available
            if self.can_post:
                success = self.tweet_poster.post_tweet(final_tweet)
                if success:
                    logging.info(f"Successfully posted viral tweet: {final_tweet}")
                else:
                    logging.error("Failed to post viral tweet")
                return success
            else:
                logging.info(f"Generated viral tweet (Twitter posting disabled): {final_tweet}")
                return True
                
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