# Social Listener

Monitor and analyze developer conversations across social platforms (Reddit, X/Twitter) to understand what the developer community is talking about today.

## Overview

Social Listener is a Python-based project that:
- Collects posts and comments from Reddit and X (Twitter)
- Stores data in a local SQLite database
- Analyzes content using Claude AI to extract sentiment, topics, and summaries
- Helps understand trending topics and pain points in the developer community

## Project Structure

```
social-listener/
├── src/
│   ├── collectors/          # Data collection modules
│   │   ├── reddit_collector.py
│   │   └── x_collector.py
│   ├── analyzers/           # Analysis modules
│   │   └── claude_analyzer.py
│   ├── database/            # Database management
│   │   └── db_manager.py
│   ├── config.py            # Configuration management
│   └── main.py              # Main entry point
├── tests/                   # Unit tests
├── data/                    # SQLite database storage
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── README.md               # This file
```

## Prerequisites

- Python 3.8+
- Reddit API credentials (free)
- Anthropic API key for Claude
- X (Twitter) API credentials (optional, requires paid access)

## Setup Instructions

### 1. Clone and Setup

```bash
cd social-listener
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Get API Credentials

#### Reddit API
1. Go to https://www.reddit.com/prefs/apps
2. Create a new app (select "script")
3. Copy your `client_id` and `client_secret`
4. Note: You can use any username as your user agent

#### Anthropic API
1. Visit https://console.anthropic.com
2. Create an API key
3. Keep it secure!

#### X (Twitter) API (Optional)
- Requires paid API access ($100+/month for meaningful rate limits)
- Start with Reddit and Claude for learning

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```
REDDIT_CLIENT_ID=your_value
REDDIT_CLIENT_SECRET=your_value
ANTHROPIC_API_KEY=your_value
```

### 4. Run the Project

```bash
cd src
python main.py
```

## Usage Examples

### Collect Posts from Reddit

```python
from collectors.reddit_collector import RedditCollector

collector = RedditCollector(
    client_id="YOUR_ID",
    client_secret="YOUR_SECRET",
    user_agent="SocialListener/1.0"
)

# Collect from a subreddit
posts = collector.collect_posts("python", limit=25)

# Search for posts
results = collector.search_posts("async programming", limit=10)
```

### Analyze Content

```python
from analyzers.claude_analyzer import ClaudeAnalyzer

analyzer = ClaudeAnalyzer(api_key="YOUR_KEY")

# Analyze sentiment
sentiment = analyzer.analyze_sentiment("I love Python!")

# Extract topics
topics = analyzer.extract_topics("We're migrating from Flask to FastAPI")

# Full analysis
full_analysis = analyzer.analyze_full(post_data)
```

### Work with Database

```python
from database.db_manager import DatabaseManager

db = DatabaseManager()

# Insert a post
db.insert_post({
    "id": "unique_id",
    "platform": "reddit",
    "source": "python",
    "title": "Post title",
    "content": "Post content",
    "author": "username",
    "score": 100,
    "created_at": "2025-01-18T10:00:00"
})

# Get unprocessed posts
posts = db.get_unprocessed_posts(limit=10)

# Insert analysis results
db.insert_analysis({
    "post_id": "unique_id",
    "analysis_type": "full",
    "sentiment": "positive",
    "topics": "python,async,programming",
    "summary": "Discussion about async programming in Python"
})
```

## Learning Goals

This project is designed to teach:
- **API Integration**: Working with Reddit PRAW library and REST APIs
- **Data Management**: SQLite database design and operations
- **AI Integration**: Using Claude API for content analysis
- **Python Best Practices**: Project structure, configuration management, error handling
- **VS Code & AI Coding**: Using Copilot and AI tools for development

## Development Roadmap

- [ ] Implement X (Twitter) collector
- [ ] Add data visualization dashboard
- [ ] Create trending topics report
- [ ] Add scheduled data collection
- [ ] Build CLI for easier interaction
- [ ] Add unit tests
- [ ] Create data export functionality
- [ ] Add filtering and search capabilities

## Testing

```bash
pytest tests/
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Create a pull request

## Limitations & Notes

- **X API**: Free tier has very limited access. Consider starting with Reddit only
- **Rate Limiting**: Both APIs have rate limits; the code respects these limits
- **Data Retention**: Data is stored locally; consider privacy when sharing
- **Costs**: Anthropic API usage will incur costs based on token usage

## Resources

- [PRAW Documentation](https://praw.readthedocs.io/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [Reddit API Documentation](https://www.reddit.com/dev/api)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

## License

MIT License

## Authors

- Social Listener Team

---

**Happy Learning!** 🚀

This is a learning project. Feel free to experiment, break things, and learn. That's the whole point!
