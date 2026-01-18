"""Claude-based analyzer for Social Listener."""

import logging
import json
from typing import Dict, Optional
from anthropic import Anthropic

logger = logging.getLogger(__name__)

class ClaudeAnalyzer:
    """Analyzes social media posts and comments using Claude API."""
    
    def __init__(self, api_key: str):
        """Initialize Claude analyzer."""
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"
        logger.info("Claude analyzer initialized")
    
    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze the sentiment of text.
        
        Returns:
            Dict with sentiment and confidence
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Analyze the sentiment of this text. 
                        Respond ONLY with a JSON object like: {{"sentiment": "positive/neutral/negative", "confidence": 0.95}}
                        
                        Text: {text}"""
                    }
                ]
            )
            
            response_text = message.content[0].text
            result = json.loads(response_text)
            return result
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {"sentiment": "unknown", "confidence": 0}
    
    def extract_topics(self, text: str) -> Dict:
        """
        Extract topics and keywords from text.
        
        Returns:
            Dict with identified topics and technologies
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Extract the main topics and technologies discussed. 
                        Respond ONLY with a JSON object like: {{"topics": ["topic1", "topic2"], "technologies": ["tech1", "tech2"]}}
                        
                        Text: {text}"""
                    }
                ]
            )
            
            response_text = message.content[0].text
            result = json.loads(response_text)
            return result
        except Exception as e:
            logger.error(f"Error extracting topics: {e}")
            return {"topics": [], "technologies": []}
    
    def summarize(self, text: str, max_length: int = 200) -> Dict:
        """
        Summarize text content.
        
        Returns:
            Dict with summary
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": f"""Summarize this text in {max_length} characters or less. 
                        Respond ONLY with a JSON object like: {{"summary": "brief summary"}}
                        
                        Text: {text}"""
                    }
                ]
            )
            
            response_text = message.content[0].text
            result = json.loads(response_text)
            return result
        except Exception as e:
            logger.error(f"Error summarizing: {e}")
            return {"summary": "Unable to summarize"}
    
    def analyze_full(self, post_data: Dict) -> Dict:
        """
        Perform comprehensive analysis on a post.
        
        Returns:
            Dict with full analysis results
        """
        text = f"{post_data.get('title', '')} {post_data.get('content', '')}"
        
        results = {
            "post_id": post_data.get("id"),
            "sentiment": self.analyze_sentiment(text),
            "topics": self.extract_topics(text),
            "summary": self.summarize(text),
        }
        
        return results
