import os
import random
import logging
from typing import List, Dict

from dotenv import load_dotenv
from youtube_search_python import VideosSearch
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import requests
from openai import OpenAI

from tweet_poster import TweetPoster

load_dotenv()

logger = logging.getLogger(__name__)


class YouTubeTweetGenerator:
    """Generate and post an AI/LLM related tweet based on YouTube video transcript."""

    def __init__(self):
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.deepseek_api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable is required")
        self.client = OpenAI(api_key=self.deepseek_api_key, base_url="https://api.deepseek.com")

        self.tinyurl_api_key = os.getenv("TINYURL_API_KEY")
        if not self.tinyurl_api_key:
            raise ValueError("TINYURL_API_KEY environment variable is required")

        try:
            self.poster = TweetPoster()
            self.can_post = True
        except Exception as exc:
            logger.warning(f"TweetPoster unavailable: {exc}")
            self.poster = None
            self.can_post = False

        # Query keywords pool
        self.keywords_pool: List[str] = [
            "LLM", "Large Language Model", "OpenAI GPT", "生成AI", "人工知能", "AI Revolution",
        ]

    # ---------------------------------------------------------------------
    # YouTube helpers
    # ---------------------------------------------------------------------
    def search_video(self) -> Dict[str, str]:
        """Search YouTube for a video and return {title, video_id, url}."""
        keywords = random.choice(self.keywords_pool)
        result = VideosSearch(keywords, limit=10).result().get("result", [])
        random.shuffle(result)
        for video in result:
            video_id = video.get("id")
            url = f"https://www.youtube.com/watch?v={video_id}"
            title = video.get("title", "")
            if video_id:
                logger.info(f"Chosen video: {title} ({url})")
                return {"title": title, "video_id": video_id, "url": url}
        raise RuntimeError("No suitable YouTube video found")

    def get_transcript(self, video_id: str, max_chars: int = 2000) -> str:
        """Fetch English transcript and truncate to max_chars."""
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en", "ja"])
            text = " ".join([seg["text"] for seg in transcript])
            return text[:max_chars]
        except TranscriptsDisabled:
            raise RuntimeError("Transcript disabled for this video")
        except Exception as exc:
            raise RuntimeError(f"Transcript retrieval failed: {exc}")

    # ---------------------------------------------------------------------
    # TinyURL helper
    # ---------------------------------------------------------------------
    def shorten_url(self, long_url: str) -> str:
        api_url = "https://api.tinyurl.com/create"
        headers = {"Authorization": f"Bearer {self.tinyurl_api_key}", "Content-Type": "application/json"}
        payload = {"url": long_url, "domain": "tinyurl.com"}
        resp = requests.post(api_url, json=payload, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()["data"]["tiny_url"]

    # ---------------------------------------------------------------------
    # Tweet generation
    # ---------------------------------------------------------------------
    def summarize_to_tweet(self, transcript: str, video_title: str, short_url: str) -> str:
        prompt = (
            "You are a top-tier viral content creator in the AI domain. Your task:\n"
            "- Craft ONE punchy English tweet (≤280 characters) that can go viral.\n"
            "- Summarise the most compelling insight from the YouTube video below.\n"
            "- Use ONLY the following keywords (include at least three, exactly as written): Training Data, Bias, Hallucination, AI Ethics, Responsible AI, Hyperparameter Tuning, Inference, Overfitting, Alignment, AI Safety, Explainable AI (XAI).\n"
            "- Do NOT introduce other AI buzzwords or meta-information.\n"
            "- Add 2–3 relevant hashtags.\n"
            "- End with the shortened URL provided.\n"
            "\n[Video Title]\n" + video_title + "\n\n[Transcript Excerpt]\n" + transcript[:500] + "\n\n[Short URL]\n" + short_url
        )

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.8,
        )
        tweet = response.choices[0].message.content.strip()
        # Ensure length <=280
        if len(tweet) > 280:
            tweet = tweet[:279]
        return tweet

    # ---------------------------------------------------------------------
    def run(self):
        try:
            video_info = self.search_video()
            transcript = self.get_transcript(video_info["video_id"])
            short_url = self.shorten_url(video_info["url"])
            tweet = self.summarize_to_tweet(transcript, video_info["title"], short_url)
            logger.info(f"Generated tweet: {tweet}")
            if self.can_post:
                success = self.poster.post_tweet(tweet)
                if success:
                    logger.info("Tweet posted successfully")
                else:
                    logger.error("Tweet post failed")
        except Exception as exc:
            logger.error(f"YouTubeTweetGenerator failed: {exc}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    generator = YouTubeTweetGenerator()
    generator.run()