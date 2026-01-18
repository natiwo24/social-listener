# Social Listener - VS Code Copilot Instructions

This is a learning project to help developers understand:
- API integration (Reddit PRAW, X/Twitter APIs)
- Database design and management (SQLite)
- AI integration (Claude API)
- Project structure and Python best practices
- VS Code and AI-assisted coding workflows

## Project Overview

Social Listener collects and analyzes developer conversations from Reddit and X (Twitter) to understand what the developer community is discussing.

## Key Learning Areas

1. **API Integration**: Learn to authenticate and use external APIs
2. **Data Management**: SQLite database for persistent storage
3. **AI Integration**: Claude API for sentiment analysis and topic extraction
4. **Configuration Management**: Environment variables and secure credential handling
5. **Testing**: Unit tests for core functionality

## For AI Assistance

When providing suggestions or code:
- Focus on teaching concepts, not just solving problems
- Explain why certain approaches are used
- Highlight Python best practices
- Reference the project structure and existing patterns
- Suggest improvements for code quality and maintainability

## Project Structure Reference

- `src/collectors/` - Data collection modules (Reddit, X)
- `src/analyzers/` - Analysis using Claude API
- `src/database/` - SQLite database management
- `src/config.py` - Configuration and environment variables
- `tests/` - Unit tests
- `data/` - SQLite database file location

## Common Tasks

### Add a new collector
1. Create file in `src/collectors/`
2. Follow RedditCollector pattern
3. Add to `__init__.py`

### Add analysis features
1. Create method in `ClaudeAnalyzer`
2. Follow existing sentiment/topic methods
3. Update `main.py` to use new features

### Database changes
1. Update schema in `DatabaseManager.init_db()`
2. Add insert/query methods
3. Test with `tests/test_db_manager.py`

## Setup Requirements

Before running:
1. Copy `.env.example` to `.env`
2. Fill in API credentials
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `cd src && python main.py`

## Helpful Tips

- Start with Reddit collector (easier than X API)
- Claude API costs money; test with small amounts first
- SQLite is perfect for local development
- Use logging to debug data collection
- Test database operations before full runs
