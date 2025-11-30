"""Conversation Summarizer - No API Required"""

class ConversationSummarizer:
    """Summarize conversations using keyword extraction"""
    
    @staticmethod
    def summarize(messages: list) -> dict:
        """Generate conversation summary"""
        if not messages:
            return {
                'total_messages': 0,
                'user_messages': 0,
                'bot_messages': 0,
                'topics': [],
                'sentiment_overview': 'N/A'
            }
        
        user_messages = [m for m in messages if m['role'] == 'user']
        bot_messages = [m for m in messages if m['role'] == 'assistant']
        
        # Extract common words (simple keyword extraction)
        all_text = ' '.join([m['content'].lower() for m in user_messages])
        
        common_words = ['shipping', 'return', 'product', 'order', 'payment', 
                       'track', 'refund', 'warranty', 'electronics', 'fashion']
        
        topics = [word for word in common_words if word in all_text]
        
        # Sentiment overview
        sentiments = []
        for msg in bot_messages:
            if 'data' in msg and 'sentiment' in msg['data']:
                sentiments.append(msg['data']['sentiment']['sentiment'])
        
        if sentiments:
            positive_count = sentiments.count('Positive')
            negative_count = sentiments.count('Negative')
            if positive_count > negative_count:
                sentiment_overview = '😊 Mostly Positive'
            elif negative_count > positive_count:
                sentiment_overview = '😞 Some Concerns'
            else:
                sentiment_overview = '😐 Neutral'
        else:
            sentiment_overview = '😐 Neutral'
        
        return {
            'total_messages': len(messages),
            'user_messages': len(user_messages),
            'bot_messages': len(bot_messages),
            'topics': topics[:5],  # Top 5 topics
            'sentiment_overview': sentiment_overview
        }