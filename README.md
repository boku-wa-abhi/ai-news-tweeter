# 🤖 AI News Tweeter




An automated Python system that fetches the latest AI/LLM news, summarizes articles using DeepSeek API, and posts engaging tweets using GitHub Actions. The system also includes a viral tweet generator that creates attention-grabbing AI-related tweets.

## 🚀 Features

- **Automated News Fetching**: Fetches AI/LLM news from reputable sources via NewsAPI
- **AI-Powered Summarization**: Uses DeepSeek API to create concise, engaging summaries
- **Smart Tweet Formatting**: Automatically formats tweets with hashtags and URLs (≤280 characters)
- **Viral Tweet Generation**: Creates engaging, viral-style tweets about AI topics
- **CSV-Based Tweet Scheduling**: Posts pre-written AI safety and governance tweets based on scheduled dates
- **Duplicate Prevention**: Tracks posted articles to avoid duplicates
- **Scheduled Automation**: Runs daily via GitHub Actions
- **Comprehensive Logging**: Tracks all activities and posted tweets

## 📁 Project Structure

```
ai-news-tweeter/
├── main.py                     # Main orchestrator script for news tweets
├── main_1.py                   # Alternative main script with viral tweet generation
├── news_fetcher.py             # Fetches AI/LLM news from NewsAPI
├── tweet_formatter.py          # Summarizes and formats tweets
├── tweet_poster.py             # Posts tweets to Twitter
├── viral_tweet_generator.py    # Generates viral AI-related tweets
├── csv_tweet_generator.py      # Posts scheduled tweets from CSV data
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variables
├── .github/
│   └── workflows/
│       ├── tweet.yml           # GitHub Actions workflow for news tweets
│       ├── viral_tweet.yml     # GitHub Actions workflow for viral tweets
│       └── csv_tweet.yml       # GitHub Actions workflow for CSV-based tweets
├── .gitignore                  # Git ignore file
└── README.md                   # This file
```

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-news-tweeter.git
cd ai-news-tweeter
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up API Keys

You'll need to obtain API keys from:

#### DeepSeek API
1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Create an account and generate an API key
3. Note down your `DEEPSEEK_API_KEY`

#### Twitter API
1. Apply for Twitter Developer access at [developer.twitter.com](https://developer.twitter.com/)
2. Create a new app and generate:
   - `TWITTER_API_KEY` (or `TWITTER_CONSUMER_KEY`)
   - `TWITTER_API_SECRET` (or `TWITTER_CONSUMER_SECRET`)
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_TOKEN_SECRET` (or `TWITTER_ACCESS_SECRET`)

#### NewsAPI (for news fetching)
1. Visit [NewsAPI](https://newsapi.org/)
2. Create an account and generate an API key
3. Note down your `NEWSAPI_KEY`

#### TinyURL API (optional, for URL shortening)
1. Visit [TinyURL Developer](https://tinyurl.com/app/dev)
2. Create an account and generate an API key
3. Note down your `TINYURL_API_KEY`

### 4. Configure GitHub Secrets

In your GitHub repository, go to Settings → Secrets and Variables → Actions, and add:

- `DEEPSEEK_API_KEY`
- `TWITTER_CONSUMER_KEY` (or `TWITTER_API_KEY`)
- `TWITTER_CONSUMER_SECRET` (or `TWITTER_API_SECRET`)
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_SECRET` (or `TWITTER_ACCESS_TOKEN_SECRET`)
- `NEWSAPI_KEY`
- `TINYURL_API_KEY` (optional)

### 5. Local Testing (Optional)

For local testing, create a `.env` file (you can copy from `.env.example`):

```bash
# DeepSeek API
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com

# Twitter API
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# NewsAPI
NEWSAPI_KEY=your_newsapi_key

# TinyURL API (optional)
TINYURL_API_KEY=your_tinyurl_api_key
```

Then run one of the following:

```bash
# For news tweets only
python main.py

# For news tweets and viral tweets
python main_1.py

# For viral tweets only
python -c "from viral_tweet_generator import ViralTweetGenerator, main; main()"

# For CSV-based scheduled tweets
python csv_tweet_generator.py
```

## 🔄 How It Works

### News Tweet Generation

1. **News Fetching**: Uses NewsAPI to fetch AI-related articles from major tech news sources
2. **Content Filtering**: Identifies AI/LLM-related articles using comprehensive keyword matching
3. **Deduplication**: Checks against previously posted articles
4. **Summarization**: Uses DeepSeek API to create engaging summaries
5. **Tweet Formatting**: Formats content with hashtags, preserves original URLs for rich link previews, and ensures ≤280 characters
6. **Publishing**: Posts tweets to Twitter and logs the activity

### Viral Tweet Generation

1. **Hook Selection**: Randomly selects from a curated list of attention-grabbing AI-related hooks
2. **Emotion Selection**: Randomly selects an emotion to evoke in the tweet
3. **Tweet Generation**: Uses DeepSeek API to generate a viral-style tweet that incorporates the hook and emotion
4. **Character Limit Check**: Ensures the tweet is within Twitter's 280 character limit
5. **Publishing**: Posts the viral tweet to Twitter and logs the activity

### CSV-Based Tweet Generation

1. **Date Matching**: Checks current date against CSV data entries
2. **Content Retrieval**: Retrieves pre-written tweet content for the current date
3. **Tweet Validation**: Ensures tweet content is within Twitter's character limits
4. **Publishing**: Posts the scheduled tweet to Twitter and logs the activity

## 📊 News Sources

The system fetches AI news via NewsAPI from these major tech news sources:

- **TechCrunch**: Technology startup and innovation news
- **Wired**: Technology and digital culture
- **Ars Technica**: Technology news and analysis
- **The Verge**: Technology and digital culture
- **VentureBeat**: Technology and startup news
- **ZDNet**: Business technology news
- **Engadget**: Consumer technology news
- **Mashable**: Technology and digital culture
- **The Next Web**: Technology and internet news
- **IEEE**: Technology and engineering news

The system uses a comprehensive list of AI-related keywords to filter articles, including terms related to:

- Core AI & ML concepts
- Large Language Models (LLMs)
- Natural Language Processing (NLP)
- AI tools and libraries
- Autonomous agents
- Conversational AI
- AI research and models
- AI applications
- AI trends and ecosystem
- Industry news and companies

## 🤖 Automation Schedule

The system runs automatically via GitHub Actions:
- **News Tweets**: Daily at 6:00 AM JST (21:00 UTC previous day)
- **Viral Tweets**: Daily at 12:00 PM JST (03:00 UTC)
- **CSV Scheduled Tweets**: Daily at 6:00 AM JST (21:00 UTC previous day)

You can also trigger any workflow manually from the GitHub Actions tab using the workflow_dispatch event.

## 📝 Logging & Monitoring

- **tweet_log.txt**: General application logs
- **posted_articles.json**: Tracks posted article URLs
- **posted_tweets.json**: History of posted tweets (from both news and viral tweet generators)

Logs are automatically uploaded as GitHub Actions artifacts after each run.

## 🔧 Customization

### Modifying News Sources

Edit the domains parameter in `news_fetcher.py` to change the news sources:

```python
params = {
    # ...
    'domains': 'techcrunch.com,wired.com,your-domain.com'
}
```

### Modifying Keywords

Update the `ai_keywords` list in `news_fetcher.py` to change content filtering:

```python
self.ai_keywords = [
    'AI', 'artificial intelligence', 'your_keyword'
]
```

### Customizing Viral Tweets

Edit the `hooks` and `emotions` lists in `viral_tweet_generator.py` to customize viral tweet generation:

```python
self.hooks = [
    "Your attention-grabbing hook here.",
    # Add more hooks...
]

self.emotions = [
    "Emotion1", "Emotion2", "Your emotion here"
    # Add more emotions...
]
```

### Changing Schedule

Modify the cron expressions in `.github/workflows/tweet.yml`:

```yaml
schedule:
  - cron: '0 12 * * *'  # Daily at noon UTC
```

## 🚨 Error Handling

### News Tweet Generator
- **API Failures**: Graceful fallback to simple summarization if DeepSeek API fails
- **Rate Limiting**: Built-in retry logic for Twitter API
- **Network Issues**: Comprehensive error logging
- **Invalid Content**: Content validation before posting

### Viral Tweet Generator
- **API Failures**: Comprehensive error logging if DeepSeek API fails
- **Character Limit**: Automatic truncation of tweets exceeding 280 characters
- **Twitter API Issues**: Detailed error logging for debugging
- **Content Validation**: Ensures tweets meet Twitter's requirements

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

- Ensure compliance with Twitter's Terms of Service
- Respect rate limits and API usage guidelines
- Monitor your bot's activity regularly
- Be mindful of content quality and relevance

## 💻 Code Architecture

### Main Components

1. **NewsFetcher (`news_fetcher.py`)**
   - Fetches AI-related news articles from NewsAPI
   - Filters articles based on AI keywords
   - Shortens URLs using TinyURL API (optional)
   - Handles deduplication of articles

2. **TweetFormatter (`tweet_formatter.py`)**
   - Summarizes articles using DeepSeek API
   - Formats tweets with appropriate hashtags
   - Ensures tweets are within character limits
   - Provides fallback summarization if API fails

3. **TweetPoster (`tweet_poster.py`)**
   - Posts tweets to Twitter using Tweepy
   - Handles Twitter API authentication
   - Logs posted tweets
   - Provides error handling for Twitter API

4. **ViralTweetGenerator (`viral_tweet_generator.py`)**
   - Generates viral-style tweets about AI topics
   - Uses hooks and emotions to create engaging content
   - Leverages DeepSeek API for natural language generation
   - Ensures tweets are within character limits

5. **CSVTweetGenerator (`csv_tweet_generator.py`)**
   - Reads pre-written tweets from CSV file
   - Matches tweets to current date
   - Posts scheduled AI safety and governance content
   - Handles missing dates gracefully

6. **Main Orchestrators**
   - `main.py`: Orchestrates news tweet generation
   - `main_1.py`: Orchestrates both news and viral tweet generation
   - `csv_tweet_generator.py`: Standalone CSV-based tweet generation

### Implementation Details

- **Modular Design**: Each component is encapsulated in its own class with clear responsibilities
- **Error Handling**: Comprehensive try-except blocks with detailed logging
- **API Integration**: Clean interfaces to external APIs (Twitter, DeepSeek, NewsAPI)
- **Configuration**: Environment variables for all API keys and settings
- **Logging**: Detailed logging for debugging and monitoring

## 🆘 Troubleshooting

### Common Issues

1. **Authentication Errors**: Verify all API keys are correctly set in GitHub Secrets
2. **No Articles Found**: Check if NewsAPI is returning results for your keywords
3. **Tweet Too Long**: The formatter automatically truncates, but manual adjustment may be needed
4. **Rate Limiting**: The system includes built-in rate limit handling
5. **DeepSeek API Errors**: Check your API key and usage limits

### Getting Help

If you encounter issues not covered in the troubleshooting section, please open an issue on GitHub with detailed information about the problem.

## 🚀 Future Enhancements

### Planned Features

1. **Analytics Dashboard**: Track tweet performance and engagement metrics
2. **Content Optimization**: A/B testing of different tweet formats and styles
3. **Multi-platform Support**: Extend to other social media platforms (LinkedIn, Mastodon)
4. **Advanced Filtering**: Improved relevance scoring for news articles
5. **Interactive Mode**: CLI interface for manual review before posting
6. **Image Generation**: Add AI-generated images to tweets for higher engagement
7. **Sentiment Analysis**: Tailor tweet tone based on article sentiment
8. **Thread Support**: Create tweet threads for longer content
9. **Customizable Schedules**: Configure posting times based on audience analytics
10. **Content Curation**: Save interesting articles for later use

## 🧪 Code Quality & Best Practices

This project follows several software development best practices:

1. **Modular Architecture**: Each component has a single responsibility
2. **Comprehensive Error Handling**: Graceful handling of API failures and edge cases
3. **Detailed Logging**: Extensive logging for debugging and monitoring
4. **Environment Configuration**: All sensitive data and configuration stored in environment variables
5. **API Abstraction**: Clean interfaces to external services
6. **Rate Limit Handling**: Respects API rate limits to prevent service disruptions
7. **Content Validation**: Ensures generated content meets platform requirements
8. **Automated Workflow**: CI/CD pipeline for regular execution
9. **Fallback Mechanisms**: Alternative approaches when primary methods fail
10. **Documentation**: Comprehensive README and code comments

If you encounter issues:
1. Check the GitHub Actions logs
2. Review the uploaded log artifacts
3. Open an issue with detailed error information

---

**Happy Tweeting! 🐦✨**
