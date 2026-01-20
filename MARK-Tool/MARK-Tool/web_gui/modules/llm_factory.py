"""
LLM Factory - Factory pattern for creating LLM manager instances

This factory handles the creation of different LLM manager implementations,
following the Factory design pattern for better extensibility.
"""

import logging
from typing import Dict, Type
from dataclasses import dataclass
from typing import Optional

from .textGenerationManager import TextGenerationManager
from .lmstudio_manager import LMStudioManager


logger = logging.getLogger(__name__)


@dataclass
class LLMConfig:
    """
    Configuration dataclass for LLM settings.
    
    Centralizes all LLM-related configuration in a single, type-safe object.
    """
    llm_type: str = 'lmstudio'
    base_url: str = 'http://localhost:1234/v1'
    model: str = 'local-model'
    temperature: float = 0.3
    max_tokens: int = 2000
    timeout: int = 300
    api_key: Optional[str] = None
    starting_prompt: str = ""
    
    def __post_init__(self):
        """Validate configuration after initialization"""
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError(f"Temperature must be between 0 and 2, got {self.temperature}")
        
        if self.max_tokens < 1:
            raise ValueError(f"max_tokens must be positive, got {self.max_tokens}")
        
        if self.timeout < 1:
            raise ValueError(f"timeout must be positive, got {self.timeout}")


class LLMFactory:
    """
    Factory for creating LLM manager instances.
    
    Implements the Factory pattern to decouple LLM provider selection
    from the service layer. Makes it easy to add new LLM providers
    without modifying existing code (Open/Closed Principle).
    """
    
    # Registry of available LLM managers
    _managers: Dict[str, Type[TextGenerationManager]] = {
        'lmstudio': LMStudioManager,
        # Easy to add more:
        # 'openai': OpenAIManager,
        # 'anthropic': AnthropicManager,
        # 'ollama': OllamaManager,
    }
    
    @classmethod
    def create_manager(cls, config: LLMConfig) -> TextGenerationManager:
        """
        Create an LLM manager instance based on configuration.
        
        Args:
            config: LLMConfig instance with provider settings
            
        Returns:
            Initialized LLM manager instance
            
        Raises:
            ValueError: If llm_type is not supported
        """
        manager_class = cls._managers.get(config.llm_type)
        
        if not manager_class:
            available = ', '.join(cls._managers.keys())
            raise ValueError(
                f"Unsupported LLM type: '{config.llm_type}'. "
                f"Available types: {available}"
            )
        
        logger.info(f"Creating {config.llm_type} manager with model: {config.model}")
        
        # Create manager with appropriate parameters based on type
        if config.llm_type == 'lmstudio':
            return manager_class(
                base_url=config.base_url,
                model=config.model,
                starting_prompt=config.starting_prompt,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                timeout=config.timeout
            )
        # When adding new providers, add their specific initialization here:
        # elif config.llm_type == 'openai':
        #     return manager_class(
        #         api_key=config.api_key,
        #         model=config.model,
        #         ...
        #     )
        else:
            # Fallback for future providers
            return manager_class(
                model=config.model,
                starting_prompt=config.starting_prompt
            )
    
    @classmethod
    def register_manager(cls, llm_type: str, manager_class: Type[TextGenerationManager]):
        """
        Register a new LLM manager type.
        
        Allows dynamic registration of new providers at runtime.
        
        Args:
            llm_type: Unique identifier for the LLM type
            manager_class: Manager class implementing TextGenerationManager
        """
        if not issubclass(manager_class, TextGenerationManager):
            raise TypeError(
                f"Manager class must inherit from TextGenerationManager, "
                f"got {manager_class.__name__}"
            )
        
        cls._managers[llm_type] = manager_class
        logger.info(f"Registered new LLM manager type: {llm_type}")
    
    @classmethod
    def get_available_types(cls) -> list:
        """
        Get list of available LLM types.
        
        Returns:
            List of registered LLM type identifiers
        """
        return list(cls._managers.keys())
    
    @classmethod
    def is_supported(cls, llm_type: str) -> bool:
        """
        Check if an LLM type is supported.
        
        Args:
            llm_type: LLM type identifier to check
            
        Returns:
            True if supported, False otherwise
        """
        return llm_type in cls._managers
