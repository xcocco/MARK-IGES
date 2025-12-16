"""
LM Studio Manager - Local LLM adapter

This module provides integration with LM Studio for local LLM inference.
"""

import logging
import requests

from .textGenerationManager import TextGenerationManager


logger = logging.getLogger(__name__)


class LMStudioManager(TextGenerationManager):
    """
    Manager for LM Studio local LLM.
    """
    
    def __init__(
        self, 
        base_url="http://localhost:1234/v1", 
        model="local-model", 
        starting_prompt="",
        temperature=0.3,
        max_tokens=2000
    ):
        """
        Initialize LM Studio manager.
        
        Args:
            base_url: LM Studio server endpoint
            model: Model identifier
            starting_prompt: System prompt for the conversation
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
        """
        super().__init__(model, starting_prompt)
        
        self.base_url = base_url.rstrip('/')
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.endpoint = f"{self.base_url}/chat/completions"
        
        logger.info(f"LM Studio manager initialized: {self.endpoint}")
    
    def api_call(self, messages):
        """
        Make API call to LM Studio.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Generated text response
        """
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
            
            response = requests.post(
                self.endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            logger.debug(f"LM Studio response: {content[:100]}...")
            return content
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error calling LM Studio: {str(e)}"
            logger.error(error_msg)
            return f"Mi dispiace, si è verificato un errore nella comunicazione con il modello LLM: {str(e)}"
        except (KeyError, IndexError) as e:
            error_msg = f"Error parsing LM Studio response: {str(e)}"
            logger.error(error_msg)
            return f"Errore nel parsing della risposta LLM: {str(e)}"
    
    def generate_response_history(self, message):
        """
        Generate response with conversation history.
        
        Args:
            message: User message
            
        Returns:
            Generated response
        """
        self.messages.append({"role": "user", "content": message})
        response = self.api_call(self.messages)
        self.messages.append({"role": "assistant", "content": response})
        return response
    
    def generate_response(self, message, starting_prompt=""):
        """
        Generate response without conversation history (one-shot).
        
        Args:
            message: User message
            starting_prompt: Optional system prompt override
            
        Returns:
            Generated response
        """
        if starting_prompt:
            msgs = [
                {"role": "system", "content": starting_prompt},
                {"role": "user", "content": message}
            ]
        else:
            msgs = [
                {"role": "system", "content": self.starting_prompt},
                {"role": "user", "content": message}
            ]
        
        return self.api_call(msgs)
    
    def test_connection(self):
        """
        Test connection to LM Studio server.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.generate_response("Hello", "You are a helpful assistant.")
            return bool(response and not response.startswith("Error") and not response.startswith("Mi dispiace"))
        except Exception as e:
            logger.error(f"LM Studio connection test failed: {e}")
            return False
    
    def get_model_info(self):
        """
        Get information about the current model.
        
        Returns:
            Dictionary with model configuration
        """
        return {
            "provider": "LM Studio",
            "base_url": self.base_url,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "connected": self.test_connection()
        }