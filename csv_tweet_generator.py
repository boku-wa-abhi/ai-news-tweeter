import os
import csv
import logging
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from tweet_poster import TweetPoster

load_dotenv()

logger = logging.getLogger(__name__)


class CSVTweetGenerator:
    """Generate and post tweets from CSV file based on current date."""

    def __init__(self, csv_file_path: str = "data/ai_safety_governance_tweets.csv"):
        self.csv_file_path = csv_file_path
        
        try:
            self.poster = TweetPoster()
            self.can_post = getattr(self.poster, "credentials_valid", False)
        except Exception as exc:
            logger.warning(f"TweetPoster unavailable: {exc}")
            self.poster = None
            self.can_post = False

    def get_tweet_for_date(self, target_date: str) -> Optional[str]:
        """Get tweet content for a specific date from CSV file.
        
        Args:
            target_date: Date in YYYY-MM-DD format
            
        Returns:
            Tweet content if found, None otherwise
        """
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['date'] == target_date:
                        return row['tweet']
            return None
        except FileNotFoundError:
            logger.error(f"CSV file not found: {self.csv_file_path}")
            return None
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            return None

    def post_tweet(self, tweet_content: str) -> bool:
        """Post tweet content to Twitter.
        
        Args:
            tweet_content: The tweet text to post
            
        Returns:
            True if posted successfully, False otherwise
        """
        if not self.can_post:
            logger.warning("Cannot post tweet - TweetPoster not available or credentials invalid")
            return False
            
        try:
            result = self.poster.post_tweet(tweet_content)
            if result:
                logger.info(f"Tweet posted successfully: {tweet_content[:50]}...")
                return True
            else:
                logger.error("Failed to post tweet")
                return False
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            return False

    def run(self):
        """Main execution method - get today's tweet and post it."""
        # Get today's date in YYYY-MM-DD format
        today = datetime.now().strftime("%Y-%m-%d")
        logger.info(f"Looking for tweet for date: {today}")
        
        # Get tweet content for today
        tweet_content = self.get_tweet_for_date(today)
        
        if not tweet_content:
            logger.warning(f"No tweet found for date: {today}")
            return
            
        logger.info(f"Found tweet for {today}: {tweet_content[:50]}...")
        
        # Post the tweet
        if self.can_post:
            success = self.post_tweet(tweet_content)
            if success:
                logger.info("Tweet generation and posting completed successfully")
            else:
                logger.error("Failed to post tweet")
        else:
            logger.info(f"Would post tweet (posting disabled): {tweet_content}")


def main():
    """Main function for standalone execution."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    generator = CSVTweetGenerator()
    generator.run()


if __name__ == "__main__":
    main()