"""Simple Sentiment Analysis - No API Required"""

class SentimentAnalyzer:
    """Analyze sentiment without external APIs"""
    
    def __init__(self):
        self.positive_words = [
            'good', 'great', 'excellent', 'amazing', 'love', 'best', 
            'fantastic', 'wonderful', 'awesome', 'perfect', 'happy',
            'satisfied', 'impressed', 'recommend', 'helpful', 'thank'
        ]
        
        self.negative_words = [
            'bad', 'terrible', 'worst', 'hate', 'awful', 'horrible',
            'disappointed', 'angry', 'frustrated', 'broken', 'defective',
            'useless', 'damaged', 'poor', 'complaint', 'refund'
        ]
    
    def analyze(self, text: str) -> dict:
        """Analyze sentiment of text"""
        text_lower = text.lower()
        
        positive_count = sum(1 for word in self.positive_words if word in text_lower)
        negative_count = sum(1 for word in self.negative_words if word in text_lower)
        
        total = positive_count + negative_count
        
        if total == 0:
            sentiment = 'Neutral'
            score = 0.5
            emoji = '😐'
        elif positive_count > negative_count:
            sentiment = 'Positive'
            score = round(positive_count / total, 2)
            emoji = '😊' if score > 0.7 else '🙂'
        elif negative_count > positive_count:
            sentiment = 'Negative'
            score = round(negative_count / total, 2)
            emoji = '😞' if score > 0.7 else '😕'
        else:
            sentiment = 'Mixed'
            score = 0.5
            emoji = '🤔'
        
        return {
            'sentiment': sentiment,
            'score': score,
            'emoji': emoji,
            'positive_words': positive_count,
            'negative_words': negative_count
        }