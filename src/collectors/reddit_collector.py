"""Reddit data collector using PRAW."""

import logging
from typing import List, Dict, Optional
from datetime import datetime
import praw

logger = logging.getLogger(__name__)

class RedditCollector:
    """Collects data from Reddit using PRAW."""
    
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        """Initialize Reddit collector."""
        try:
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )
            logger.info("Reddit collector initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Reddit collector: {e}")
            self.reddit = None
    
    def collect_posts(self, subreddit: str, limit: int = 25, time_filter: str = "day") -> List[Dict]:
        """
        Collect posts from a subreddit.
        
        Args:
            subreddit: Subreddit name
            limit: Number of posts to collect
            time_filter: Time filter ('day', 'week', 'month', 'year', 'all')
        
        Returns:
            List of post dictionaries
        """
        if not self.reddit:
            logger.error("Reddit client not initialized")
            return []
        
        posts = []
        try:
            sub = self.reddit.subreddit(subreddit)
            
            # Get hot posts from subreddit
            for post in sub.hot(time_filter=time_filter, limit=limit):
                if not post.stickied:  # Skip stickied posts
                    posts.append(self._parse_post(post, subreddit))
            
            logger.info(f"Collected {len(posts)} posts from r/{subreddit}")
        except Exception as e:
            logger.error(f"Error collecting posts from r/{subreddit}: {e}")
        
        return posts
    
    def collect_post_comments(self, submission_id: str, limit: int = 50) -> List[Dict]:
        """
        Collect comments from a specific post.
        
        Args:
            submission_id: Reddit submission ID
            limit: Number of comments to collect
        
        Returns:
            List of comment dictionaries
        """
        if not self.reddit:
            logger.error("Reddit client not initialized")
            return []
        
        comments = []
        try:
            submission = self.reddit.submission(id=submission_id)
            submission.comments.replace_more(limit=0)
            
            for i, comment in enumerate(submission.comments.list()):
                if i >= limit:
                    break
                comments.append(self._parse_comment(comment, submission_id))
            
            logger.info(f"Collected {len(comments)} comments from submission {submission_id}")
        except Exception as e:
            logger.error(f"Error collecting comments from {submission_id}: {e}")
        
        return comments
    
    def search_posts(self, query: str, subreddit: Optional[str] = None, limit: int = 25) -> List[Dict]:
        """
        Search for posts matching a query.
        
        Args:
            query: Search query
            subreddit: Optional subreddit to limit search
            limit: Number of results to return
        
        Returns:
            List of post dictionaries
        """
        if not self.reddit:
            logger.error("Reddit client not initialized")
            return []
        
        posts = []
        try:
            if subreddit:
                search_subreddit = self.reddit.subreddit(subreddit)
                results = search_subreddit.search(query, time_filter="day", limit=limit)
            else:
                results = self.reddit.subreddit("all").search(query, time_filter="day", limit=limit)
            
            for post in results:
                posts.append(self._parse_post(post, subreddit or "all"))
            
            logger.info(f"Found {len(posts)} posts matching '{query}'")
        except Exception as e:
            logger.error(f"Error searching for '{query}': {e}")
        
        return posts
    
    def _parse_post(self, submission, subreddit: str) -> Dict:
        """Parse a PRAW submission object into a dictionary."""
        return {
            "id": f"reddit_{submission.id}",
            "platform": "reddit",
            "source": subreddit,
            "title": submission.title,
            "content": submission.selftext,
            "author": submission.author.name if submission.author else "[deleted]",
            "url": submission.url,
            "score": submission.score,
            "created_at": datetime.fromtimestamp(submission.created_utc).isoformat(),
        }
    
    def _parse_comment(self, comment, post_id: str) -> Dict:
        """Parse a PRAW comment object into a dictionary."""
        return {
            "id": f"reddit_comment_{comment.id}",
            "post_id": f"reddit_{post_id}",
            "platform": "reddit",
            "author": comment.author.name if comment.author else "[deleted]",
            "content": comment.body,
            "score": comment.score,
            "created_at": datetime.fromtimestamp(comment.created_utc).isoformat(),
        }
