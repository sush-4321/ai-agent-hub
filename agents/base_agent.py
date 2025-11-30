"""Base Agent Class - All agents inherit from this"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging
from datetime import datetime

class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.created_at = datetime.now()
        self.conversation_history = []
        self.logger = logging.getLogger(agent_name)
    
    @abstractmethod
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process query - must be implemented by child classes"""
        pass
    
    def add_to_history(self, role: str, content: str):
        """Add to conversation history"""
        self.conversation_history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []