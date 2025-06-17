# 🤖 AI News Tweeter

An automated Python system that fetches the latest AI/LLM news, summarizes articles using DeepSeek API, and posts engaging tweets twice daily using GitHub Actions.

## 🚀 Features

- **Automated News Fetching**: Scrapes AI/LLM news from reputable sources (The Verge, TechCrunch, MIT Tech Review, OpenAI Blog, etc.)
- **AI-Powered Summarization**: Uses DeepSeek API to create concise, engaging summaries
- **Smart Tweet Formatting**: Automatically formats tweets with hashtags and URLs (≤280 characters)
- **Duplicate Prevention**: Tracks posted articles to avoid duplicates
- **Scheduled Automation**: Runs twice daily (9 AM & 5 PM JST) via GitHub Actions
- **Comprehensive Logging**: Tracks all activities and posted tweets

## 📁 Project Structure

```
ai-news-tweeter/
├── main.py                     # Main orchestrator script
├── news_fetcher.py             # Fetches AI/LLM news from RSS feeds
├── tweet_formatter.py          # Summarizes and formats tweets
├── tweet_poster.py             # Posts tweets to Twitter
├── requirements.txt            # Python dependencies
├── config/
│   └── __init__.py             # Config package
├── .github/
│   └── workflows/
│       └── tweet.yml           # GitHub Actions workflow
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
   - `TWITTER_CONSUMER_KEY`
   - `TWITTER_CONSUMER_SECRET`
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_SECRET`

#### TinyURL API (Optional)
1. Visit [TinyURL API](https://tinyurl.com/app/dev)
2. Create an account and generate an API key
3. Note down your `TINYURL_API_KEY`
4. If not provided, the system will use the free TinyURL service

### 4. Configure GitHub Secrets

In your GitHub repository, go to Settings → Secrets and Variables → Actions, and add:

- `DEEPSEEK_API_KEY`
- `TWITTER_CONSUMER_KEY`
- `TWITTER_CONSUMER_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_SECRET`
- `TINYURL_API_KEY` (optional)

### 5. Local Testing (Optional)

For local testing, create a `.env` file:

```bash
DEEPSEEK_API_KEY=your_deepseek_api_key
TINYURL_API_KEY=your_tinyurl_api_key
TWITTER_CONSUMER_KEY=your_twitter_consumer_key
TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_SECRET=your_twitter_access_secret
```

Then run:

```bash
python main.py
```

## 🔄 How It Works

1. **News Fetching**: Uses Google News RSS feeds to scan AI articles from major financial and tech news sources
2. **Content Filtering**: Identifies AI/LLM-related articles using comprehensive keyword matching
3. **Deduplication**: Checks against previously posted articles
4. **Summarization**: Uses DeepSeek API to create engaging summaries
5. **Tweet Formatting**: Formats content with hashtags and ensures ≤250 characters
6. **Publishing**: Posts tweets to Twitter and logs the activity

## 📊 News Sources

The system fetches AI news via Google News RSS feeds from these major sources:

- **Reuters**: Global financial and business news
- **Bloomberg**: Financial markets and business intelligence
- **Wall Street Journal**: Business and financial journalism
- **Financial Times**: International business news
- **Nikkei**: Asian business and technology news
- **TechCrunch**: Technology startup and innovation news
- **The Verge**: Technology and digital culture
- **CNBC**: Business news and market analysis
- **BBC Technology**: Technology section from BBC News
- **Associated Press**: Global news wire service

## 🤖 Automation Schedule

The system runs automatically via GitHub Actions:
- **Morning**: 9:00 AM JST (00:00 UTC)
- **Evening**: 5:00 PM JST (08:00 UTC)

You can also trigger it manually from the GitHub Actions tab.

## 📝 Logging & Monitoring

- **tweet_log.txt**: General application logs
- **posted_articles.json**: Tracks posted article URLs
- **posted_tweets.json**: History of posted tweets

Logs are automatically uploaded as GitHub Actions artifacts.

## 🔧 Customization

### Adding News Sources

Edit `news_fetcher.py` and add new RSS feeds to the `rss_feeds` list:

```python
{
    'name': 'Your Source Name',
    'url': 'https://example.com/rss.xml'
}
```

### Modifying Keywords

Update the `ai_keywords` list in `news_fetcher.py` to change content filtering:

```python
self.ai_keywords = [
    'AI', 'artificial intelligence', 'your_keyword'
]
```

### Changing Schedule

Modify the cron expressions in `.github/workflows/tweet.yml`:

```yaml
schedule:
  - cron: '0 12 * * *'  # Daily at noon UTC
```

## 🚨 Error Handling

- **API Failures**: Graceful fallback to simple summarization
- **Rate Limiting**: Built-in retry logic for Twitter API
- **Network Issues**: Comprehensive error logging
- **Invalid Content**: Content validation before posting

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

## 🆘 Troubleshooting

### Common Issues

1. **Authentication Errors**: Verify all API keys are correctly set in GitHub Secrets
2. **No Articles Found**: Check if RSS feeds are accessible and contain AI-related content
3. **Tweet Too Long**: The formatter automatically truncates, but manual adjustment may be needed
4. **Rate Limiting**: The system includes built-in rate limit handling

### Getting Help

If you encounter issues:
1. Check the GitHub Actions logs
2. Review the uploaded log artifacts
3. Open an issue with detailed error information

---

**Happy Tweeting! 🐦✨**