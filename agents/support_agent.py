"""Support Agent - Handles FAQs and escalations"""

import json
from agents.base_agent import BaseAgent
from typing import Dict, Any

class SupportAgent(BaseAgent):
    """Support Assistant for handling customer queries"""
    
    def __init__(self):
        super().__init__("SupportAgent")
        self.faqs = self._load_faqs()
        self.complex_keywords = [
            'complaint', 'damaged', 'refund', 'speak to manager',
            'urgent', 'broken', 'defective', 'not working'
        ]
        self.escalation_count = 0
    
    def _load_faqs(self) -> Dict:
        """Load FAQ database"""
        try:
            with open('data/faqs.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process support query and return appropriate response"""
        query_lower = query.lower()
        
        # Check FAQs
        for key, faq in self.faqs.items():
            keywords = faq.get('keywords', [])
            if any(kw in query_lower for kw in keywords):
                return {
                    'type': 'faq',
                    'response': f"💡 **{faq.get('category', 'Info').title()}**\n\n{faq['answer']}",
                    'escalate': False,
                    'category': faq.get('category', 'general')
                }
        
        # Check escalation
        if any(kw in query_lower for kw in self.complex_keywords):
            self.escalation_count += 1
            ticket = f"TKT-{hash(query) % 100000:05d}"
            return {
                'type': 'escalation',
                'response': f"⚠️ **Escalating to Support Team**\n\nTicket: {ticket}\n\nYou'll receive an email within 1 hour.",
                'escalate': True,
                'ticket_number': ticket
            }
        
        # General help
        return {
            'type': 'general',
            'response': """👋 **How Can I Help?**

I can assist with:
📦 Shipping & Delivery
↩️ Returns & Refunds  
💳 Payment Methods
📍 Order Tracking
🛡️ Warranties & Guarantees

What would you like to know?""",
            'escalate': False
        }