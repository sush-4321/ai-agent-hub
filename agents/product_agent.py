"""Product Agent - Recommends products"""

import json
from agents.base_agent import BaseAgent
from typing import Dict, Any, List

class ProductAgent(BaseAgent):
    """Product Recommender Agent"""
    
    def __init__(self):
        super().__init__("ProductAgent")
        self.products = self._load_products()
    
    def _load_products(self) -> Dict:
        """Load product database"""
        try:
            with open('data/products.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Get product recommendations based on query"""
        query_lower = query.lower()
        recommendations = []
        
        # Check category match
        for category, items in self.products.items():
            if category in query_lower:
                recommendations = items[:3]
                break
        
        # Price-based filtering if no category
        if not recommendations:
            all_items = [item for items in self.products.values() for item in items]
            
            if any(word in query_lower for word in ['budget', 'cheap', 'affordable']):
                recommendations = sorted(all_items, key=lambda x: x['price'])[:3]
            elif any(word in query_lower for word in ['premium', 'luxury', 'expensive']):
                recommendations = sorted(all_items, key=lambda x: x['price'], reverse=True)[:3]
            else:
                recommendations = sorted(all_items, key=lambda x: x.get('rating', 0), reverse=True)[:3]
        
        return {
            'type': 'recommendations',
            'response': '🎯 **Top Recommendations:**',
            'products': recommendations
        }
