"""
Text Generation Manager - Abstract Base Class

Copied from Smart Student Server implementation.
No modifications made to preserve compatibility.
"""

from abc import ABC, abstractmethod


class TextGenerationManager(ABC):
    """
    Abstract base class for text generation using various LLM providers.
    """
    
    def __init__(self, model, starting_prompt=""):
        """
        Initialize the text generation manager.
        
        Args:
            api_key: API key for the LLM provider (None for local models)
            model: Model identifier
            starting_prompt: System prompt to initialize the conversation
        """
        self.model = model
        self.starting_prompt = starting_prompt
        self.messages = []
        
        if starting_prompt:
            self.messages.append({
                "role": "system",
                "content": starting_prompt
            })
    
    @abstractmethod
    def api_call(self, messages):
        """
        Make an API call to the LLM provider.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            Generated text response
        """
        pass
    
    @abstractmethod
    def generate_response(self, message, starting_prompt=""):
        """
        Generate a response without conversation history.
        
        Args:
            message: User message
            starting_prompt: Optional system prompt override
            
        Returns:
            Generated response
        """
        pass
    
    @abstractmethod
    def generate_response_history(self, message):
        """
        Generate a response with conversation history.
        
        Args:
            message: User message
            
        Returns:
            Generated response
        """
        pass
    
    @abstractmethod
    def test_connection(self):
        """
        Test connection to the LLM provider.
        
        Returns:
            True if connection successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_model_info(self):
        """
        Get information about the current model.
        
        Returns:
            Dictionary with model configuration and status
        """
        pass
