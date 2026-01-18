"""Configuration management for Social Listener."""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    
    # Reddit API
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "SocialListener/1.0")
    
    # X (Twitter) API
    X_API_KEY = os.getenv("X_API_KEY")
    X_API_SECRET = os.getenv("X_API_SECRET")
    X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
    
    # Claude API
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # Database
    DB_PATH = os.getenv("DB_PATH", "./data/social_listener.db")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Default subreddits to monitor
    DEFAULT_SUBREDDITS = [
        "programming",
        "webdev",
        "learnprogramming",
        "Python",
        "javascript",
        "reactjs",
        "golang",
        "rust",
    ]
    
    # Default keywords for X search
    DEFAULT_X_KEYWORDS = [
        "web development",
        "python programming",
        "javascript",
        "API development",
        "coding tips",
    ]

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

def get_config(env: str = None) -> Config:
    """Get configuration based on environment."""
    if env is None:
        env = os.getenv("FLASK_ENV", "development")
    
    if env == "production":
        return ProductionConfig()
    return DevelopmentConfig()
