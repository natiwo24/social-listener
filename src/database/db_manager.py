"""Database manager for Social Listener."""

import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages SQLite database operations for Social Listener."""
    
    def __init__(self, db_path: str = "./data/social_listener.db"):
        """Initialize database manager."""
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self) -> None:
        """Initialize database schema."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Posts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                platform TEXT NOT NULL,
                title TEXT,
                content TEXT,
                author TEXT,
                url TEXT,
                score INTEGER DEFAULT 0,
                created_at TIMESTAMP,
                collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed INTEGER DEFAULT 0
            )
        """)
        
        # Comments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id TEXT PRIMARY KEY,
                post_id TEXT NOT NULL,
                platform TEXT NOT NULL,
                author TEXT,
                content TEXT,
                score INTEGER DEFAULT 0,
                created_at TIMESTAMP,
                collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(post_id) REFERENCES posts(id)
            )
        """)
        
        # Analysis results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id TEXT NOT NULL,
                analysis_type TEXT NOT NULL,
                sentiment TEXT,
                topics TEXT,
                summary TEXT,
                raw_analysis TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(post_id) REFERENCES posts(id)
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    
    def insert_post(self, post_data: Dict) -> bool:
        """Insert a post into the database."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR IGNORE INTO posts 
                (id, source, platform, title, content, author, url, score, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                post_data.get("id"),
                post_data.get("source"),
                post_data.get("platform"),
                post_data.get("title"),
                post_data.get("content"),
                post_data.get("author"),
                post_data.get("url"),
                post_data.get("score", 0),
                post_data.get("created_at"),
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error inserting post: {e}")
            return False
    
    def get_unprocessed_posts(self, limit: int = 10) -> List[Dict]:
        """Get unprocessed posts from database."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM posts WHERE processed = 0 LIMIT ?
            """, (limit,))
            
            posts = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return posts
        except Exception as e:
            logger.error(f"Error fetching unprocessed posts: {e}")
            return []
    
    def mark_post_processed(self, post_id: str) -> bool:
        """Mark a post as processed."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("UPDATE posts SET processed = 1 WHERE id = ?", (post_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error marking post as processed: {e}")
            return False
    
    def insert_analysis(self, analysis_data: Dict) -> bool:
        """Insert analysis results into database."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO analysis_results 
                (post_id, analysis_type, sentiment, topics, summary, raw_analysis)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                analysis_data.get("post_id"),
                analysis_data.get("analysis_type"),
                analysis_data.get("sentiment"),
                analysis_data.get("topics"),
                analysis_data.get("summary"),
                analysis_data.get("raw_analysis"),
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error inserting analysis: {e}")
            return False
