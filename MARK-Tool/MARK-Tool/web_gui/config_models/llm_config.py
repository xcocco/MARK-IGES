"""
LLM Configuration - Dataclass for LLM settings

Provides a structured configuration object for LLM services,
improving type safety and making it easier to manage settings.
"""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LLMConfig:
    """
    Configuration for LLM service.
    
    This dataclass encapsulates all LLM-related settings in a single object,
    making it easier to pass around and validate configurations.
    
    Attributes:
        llm_type: Provider type ('lmstudio', 'openai', 'anthropic', etc.)
        base_url: Base URL for the LLM API endpoint
        model: Model identifier/name
        temperature: Sampling temperature (0.0-2.0, lower = more deterministic)
        max_tokens: Maximum tokens to generate in response
        timeout: Request timeout in seconds
        api_key: API key for authenticated providers (optional for local models)
        prompts_dir: Directory containing system prompt files
    """
    
    llm_type: str = 'lmstudio'
    base_url: str = 'http://localhost:1234/v1'
    model: str = 'local-model'
    temperature: float = 0.3
    max_tokens: int = 2000
    timeout: int = 300
    api_key: Optional[str] = None
    prompts_dir: Optional[str] = None
    
    @classmethod
    def from_env(cls, prompts_dir: Optional[str] = None) -> 'LLMConfig':
        """
        Create LLMConfig from environment variables.
        
        Args:
            prompts_dir: Optional override for prompts directory
            
        Returns:
            LLMConfig instance with values from environment
            
        Environment Variables:
            LLM_TYPE: Provider type (default: 'lmstudio')
            LLM_BASE_URL: API endpoint (default: 'http://localhost:1234/v1')
            LLM_MODEL: Model name (default: 'local-model')
            LLM_TEMPERATURE: Sampling temperature (default: 0.3)
            LLM_MAX_TOKENS: Max tokens (default: 2000)
            LLM_TIMEOUT: Timeout in seconds (default: 300)
            LLM_API_KEY: API key (optional)
        """
        return cls(
            llm_type=os.environ.get('LLM_TYPE', 'lmstudio'),
            base_url=os.environ.get('LLM_BASE_URL', 'http://localhost:1234/v1'),
            model=os.environ.get('LLM_MODEL', 'local-model'),
            temperature=float(os.environ.get('LLM_TEMPERATURE', '0.3')),
            max_tokens=int(os.environ.get('LLM_MAX_TOKENS', '2000')),
            timeout=int(os.environ.get('LLM_TIMEOUT', '300')),
            api_key=os.environ.get('LLM_API_KEY'),
            prompts_dir=prompts_dir
        )
    
    @classmethod
    def from_flask_config(cls, flask_config: dict, prompts_dir: Optional[str] = None) -> 'LLMConfig':
        """
        Create LLMConfig from Flask configuration object.
        
        Args:
            flask_config: Flask app.config dictionary
            prompts_dir: Optional override for prompts directory
            
        Returns:
            LLMConfig instance with values from Flask config
        """
        return cls(
            llm_type=flask_config.get('LLM_TYPE', 'lmstudio'),
            base_url=flask_config.get('LLM_BASE_URL', 'http://localhost:1234/v1'),
            model=flask_config.get('LLM_MODEL', 'local-model'),
            temperature=flask_config.get('LLM_TEMPERATURE', 0.3),
            max_tokens=flask_config.get('LLM_MAX_TOKENS', 2000),
            timeout=flask_config.get('LLM_TIMEOUT', 300),
            api_key=flask_config.get('LLM_API_KEY'),
            prompts_dir=prompts_dir or flask_config.get('PROMPTS_DIR')
        )
    
    def to_manager_kwargs(self) -> dict:
        """
        Convert config to keyword arguments for manager initialization.
        
        Returns:
            Dictionary with manager-specific parameters
        """
        kwargs = {
            'model': self.model,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'timeout': self.timeout,
        }
        
        # Add provider-specific parameters
        if self.llm_type == 'lmstudio':
            kwargs['base_url'] = self.base_url
        elif self.llm_type in ['openai', 'anthropic']:
            kwargs['api_key'] = self.api_key
        
        return kwargs
    
    def validate(self) -> None:
        """
        Validate configuration values.
        
        Raises:
            ValueError: If configuration is invalid
        """
        if self.temperature < 0.0 or self.temperature > 2.0:
            raise ValueError(f"Temperature must be between 0.0 and 2.0, got {self.temperature}")
        
        if self.max_tokens < 1:
            raise ValueError(f"max_tokens must be positive, got {self.max_tokens}")
        
        if self.timeout < 1:
            raise ValueError(f"timeout must be positive, got {self.timeout}")
        
        if not self.llm_type:
            raise ValueError("llm_type cannot be empty")
        
        if not self.model:
            raise ValueError("model cannot be empty")
    
    def __repr__(self) -> str:
        """String representation hiding sensitive data."""
        api_key_display = "***" if self.api_key else None
        return (
            f"LLMConfig(llm_type='{self.llm_type}', "
            f"model='{self.model}', "
            f"temperature={self.temperature}, "
            f"max_tokens={self.max_tokens}, "
            f"api_key={'***' if self.api_key else None})"
        )
