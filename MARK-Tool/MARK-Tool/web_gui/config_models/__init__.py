"""
Configuration Module

This module contains configuration classes for the MARK web application.
Re-exports everything from the original config.py for backward compatibility.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import from config.py
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

# Import from the original config.py file (one level up)
from ..config import (
    Config,
    DevelopmentConfig,
    ProductionConfig,
    TestingConfig,
    config,
    get_config,
    BASE_DIR,
    PROJECT_ROOT
)

# Import from new config submodules
from .llm_config import LLMConfig

# Export everything for backward compatibility
__all__ = [
    'Config',
    'DevelopmentConfig', 
    'ProductionConfig',
    'TestingConfig',
    'config',
    'get_config',
    'BASE_DIR',
    'PROJECT_ROOT',
    'LLMConfig'
]
