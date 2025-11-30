"""Social Media Agent - Generates content"""

import json
import random
from agents.base_agent import BaseAgent
from typing import Dict, Any

class SocialAgent(BaseAgent):
    """Social Media Content Generator"""
    
    def __init__(self):
    super().__init__("SupportAgent")
    self.faqs = self._load_faqs()
    self.complex_keywords = [
        'complaint', 'damaged', 'refund', 'speak to manager',
        'urgent', 'broken', 'defective', 'not working'
    ]
    self.escalation_count = 0
    self.sentiment_analyzer = SentimentAnalyzer()  # ADD THIS LINE
    
    def _load_templates(self) -> Dict:
        """Load social media templates"""
        try:
            with open('data/social_templates.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Generate social media content"""
        query_lower = query.lower()
        
        # Determine content type
        if any(word in query_lower for word in ['engagement', 'giveaway', 'contest']):
            content_type = 'engagement'
        elif any(word in query_lower for word in ['sale', 'promo', 'discount']):
            content_type = 'promotional'
        else:
            content_type = 'product_launch'
        
        templates = self.templates.get(content_type, [])
        ideas = [{'id': i+1, 'content': t} for i, t in enumerate(templates[:3])]
        
        return {
            'type': 'social_content',
            'response': f'📱 **{content_type.replace("_", " ").title()} Ideas:**',
            'content_type': content_type,
            'ideas': ideas
        }