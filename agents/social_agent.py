"""Social Media Agent - Content Generation"""

import json
import os
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from utils.sentiment_analyzer import SentimentAnalyzer

class SocialAgent(BaseAgent):
    """Social Media Content Generation Agent"""
    
    def __init__(self):
        super().__init__("SocialAgent")
        self.templates = self._load_templates()
        self.sentiment_analyzer = SentimentAnalyzer()
    
    def _load_templates(self) -> Dict:
        """Load social media templates"""
        try:
            template_path = os.path.join('data', 'social_templates.json')
            with open(template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_templates()
    
    def _get_default_templates(self) -> Dict:
        """Return default templates if file not found"""
        return {
            "launch": [
                {
                    "id": 1,
                    "platform": "Instagram",
                    "content": "🚀 Exciting News! We're thrilled to announce our latest product launch! 🎉\n\nCheck out what's new and be among the first to experience innovation! ✨\n\n#NewLaunch #Innovation #ProductLaunch #ExcitingNews",
                    "type": "Product Launch"
                },
                {
                    "id": 2,
                    "platform": "Twitter",
                    "content": "🎊 BIG ANNOUNCEMENT! 🎊\n\nOur newest product is here and it's game-changing! Get ready to be amazed.\n\n👉 Tap the link to explore\n\n#Launch #NewProduct #Innovation",
                    "type": "Product Launch"
                },
                {
                    "id": 3,
                    "platform": "Facebook",
                    "content": "🌟 Drumroll please... 🥁\n\nWe're beyond excited to introduce our latest creation! This is what you've been waiting for.\n\nClick below to discover more! ⬇️\n\n#ProductLaunch #NewRelease #Innovation",
                    "type": "Product Launch"
                }
            ],
            "engagement": [
                {
                    "id": 1,
                    "platform": "Instagram",
                    "content": "💬 We want to hear from YOU!\n\nWhat's your favorite feature of our products? Drop a comment below! 👇\n\n#Community #CustomerLove #Engagement #YourOpinionMatters",
                    "type": "Engagement"
                },
                {
                    "id": 2,
                    "platform": "Twitter",
                    "content": "🤔 Quick question for our amazing community:\n\nIf you could add ONE feature to our product, what would it be?\n\nReply with your ideas! 💡\n\n#CommunityFirst #Innovation #CustomerFeedback",
                    "type": "Engagement"
                },
                {
                    "id": 3,
                    "platform": "Facebook",
                    "content": "❤️ Show some love!\n\nTag a friend who needs to see this! Share your experience with our products in the comments.\n\nLet's build this community together! 🙌\n\n#Community #ShareTheLove #CustomerStories",
                    "type": "Engagement"
                }
            ],
            "promotion": [
                {
                    "id": 1,
                    "platform": "Instagram",
                    "content": "🔥 FLASH SALE ALERT! 🔥\n\nUp to 50% OFF on selected items! Don't miss out on these amazing deals!\n\n⏰ Limited time only!\n👉 Shop now!\n\n#Sale #Discount #LimitedOffer #ShopNow",
                    "type": "Sale Promotion"
                },
                {
                    "id": 2,
                    "platform": "Twitter",
                    "content": "💰 SPECIAL OFFER 💰\n\nGET 50% OFF TODAY ONLY!\n\nUse code: SAVE50\n\n⚡ Hurry! Offer ends at midnight!\n\n#Sale #Discount #SpecialOffer #SaveMoney",
                    "type": "Sale Promotion"
                },
                {
                    "id": 3,
                    "platform": "Facebook",
                    "content": "🎁 EXCLUSIVE DEAL for our amazing community! 🎁\n\nEnjoy up to 50% OFF on your favorite products!\n\n✨ This weekend only!\n🛍️ Click below to start shopping!\n\n#WeekendSale #SpecialDiscount #ShopNow",
                    "type": "Sale Promotion"
                }
            ],
            "general": [
                {
                    "id": 1,
                    "platform": "Multi-Platform",
                    "content": "✨ Thank you for being part of our journey!\n\nYour support means everything to us. 💙\n\n#ThankYou #Community #CustomerAppreciation",
                    "type": "Appreciation"
                },
                {
                    "id": 2,
                    "platform": "Multi-Platform",
                    "content": "🌟 Behind the scenes glimpse!\n\nHere's what goes into making your favorite products. We love what we do! ❤️\n\n#BehindTheScenes #OurStory #Passion",
                    "type": "Behind The Scenes"
                },
                {
                    "id": 3,
                    "platform": "Multi-Platform",
                    "content": "💡 Pro Tip!\n\nDid you know you can get more out of your product with this simple trick? Check it out!\n\n#ProTip #Tutorial #HowTo",
                    "type": "Educational"
                }
            ]
        }
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Generate social media content based on query"""
        query_lower = query.lower()
        
        # Analyze sentiment
        sentiment = self.sentiment_analyzer.analyze(query)
        
        # Determine content type
        if any(word in query_lower for word in ['launch', 'announce', 'new product', 'introduce']):
            content_type = 'launch'
            title = '🚀 Product Launch Ideas'
        elif any(word in query_lower for word in ['engagement', 'interact', 'community', 'question']):
            content_type = 'engagement'
            title = '💬 Engagement Content Ideas'
        elif any(word in query_lower for word in ['sale', 'promo', 'discount', 'offer', 'deal']):
            content_type = 'promotion'
            title = '🔥 Promotional Content Ideas'
        else:
            content_type = 'general'
            title = '✨ Content Ideas'
        
        # Get templates
        ideas = self.templates.get(content_type, self.templates['general'])
        
        response = f"{title}\n\nHere are 3 ready-to-use social media posts:"
        
        return {
            'type': 'social_content',
            'response': response,
            'ideas': ideas,
            'content_type': content_type,
            'sentiment': sentiment
        }