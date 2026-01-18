"""Tests for database manager."""

import unittest
import tempfile
import os
from pathlib import Path
from src.database.db_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    """Test cases for DatabaseManager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.test_db.close()
        self.db = DatabaseManager(self.test_db.name)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_db.name):
            os.unlink(self.test_db.name)
    
    def test_database_initialization(self):
        """Test that database initializes correctly."""
        self.assertTrue(os.path.exists(self.test_db.name))
    
    def test_insert_post(self):
        """Test inserting a post."""
        post_data = {
            "id": "test_post_1",
            "platform": "reddit",
            "source": "python",
            "title": "Test Post",
            "content": "This is a test post",
            "author": "testuser",
            "score": 10,
            "created_at": "2025-01-18T10:00:00"
        }
        
        result = self.db.insert_post(post_data)
        self.assertTrue(result)
    
    def test_get_unprocessed_posts(self):
        """Test retrieving unprocessed posts."""
        post_data = {
            "id": "test_post_2",
            "platform": "reddit",
            "source": "python",
            "title": "Test Post 2",
            "content": "This is another test post",
            "author": "testuser",
            "score": 20,
            "created_at": "2025-01-18T11:00:00"
        }
        
        self.db.insert_post(post_data)
        posts = self.db.get_unprocessed_posts(limit=10)
        
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]["id"], "test_post_2")
    
    def test_mark_post_processed(self):
        """Test marking a post as processed."""
        post_data = {
            "id": "test_post_3",
            "platform": "reddit",
            "source": "python",
            "title": "Test Post 3",
            "content": "Test content",
            "author": "testuser",
            "score": 30,
            "created_at": "2025-01-18T12:00:00"
        }
        
        self.db.insert_post(post_data)
        result = self.db.mark_post_processed("test_post_3")
        
        self.assertTrue(result)
        posts = self.db.get_unprocessed_posts(limit=10)
        self.assertEqual(len(posts), 0)

if __name__ == "__main__":
    unittest.main()
