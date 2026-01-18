"""Main entry point for Social Listener."""

import logging
from config import get_config
from collectors.reddit_collector import RedditCollector
from analyzers.claude_analyzer import ClaudeAnalyzer
from database.db_manager import DatabaseManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run Social Listener."""
    logger.info("Starting Social Listener...")
    
    # Load configuration
    config = get_config()
    
    # Initialize components
    db = DatabaseManager(config.DB_PATH)
    
    reddit_collector = RedditCollector(
        client_id=config.REDDIT_CLIENT_ID,
        client_secret=config.REDDIT_CLIENT_SECRET,
        user_agent=config.REDDIT_USER_AGENT
    )
    
    claude_analyzer = ClaudeAnalyzer(api_key=config.ANTHROPIC_API_KEY)
    
    logger.info("All components initialized successfully")
    
    # Example: Collect posts from subreddits
    logger.info("Collecting posts from subreddits...")
    for subreddit in config.DEFAULT_SUBREDDITS[:2]:  # Start with 2 subreddits
        posts = reddit_collector.collect_posts(subreddit, limit=5)
        
        for post in posts:
            # Store post in database
            db.insert_post(post)
            logger.info(f"Stored post: {post['title'][:50]}...")
    
    # Example: Analyze unprocessed posts
    logger.info("Analyzing posts...")
    unprocessed_posts = db.get_unprocessed_posts(limit=3)
    
    for post in unprocessed_posts:
        logger.info(f"Analyzing: {post['title'][:50]}...")
        
        # Perform analysis
        analysis = claude_analyzer.analyze_full(post)
        
        # Store analysis results
        db.insert_analysis({
            "post_id": post["id"],
            "analysis_type": "full",
            "sentiment": analysis["sentiment"].get("sentiment"),
            "topics": ",".join(analysis["topics"].get("topics", [])),
            "summary": analysis["summary"].get("summary"),
            "raw_analysis": str(analysis),
        })
        
        # Mark post as processed
        db.mark_post_processed(post["id"])
        logger.info(f"Completed analysis for post: {post['id']}")
    
    logger.info("Social Listener completed")

if __name__ == "__main__":
    main()
