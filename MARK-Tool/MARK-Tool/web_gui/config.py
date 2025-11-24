"""
Flask Application Configuration
"""
import os
from pathlib import Path

# Base directory of the web_gui module
BASE_DIR = Path(__file__).parent.absolute()

# Base directory of the MARK-Tool project
PROJECT_ROOT = BASE_DIR.parent


class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB max file size
    ALLOWED_EXTENSIONS = {'csv'}
    
    # Analysis settings
    DEFAULT_INPUT_PATH = os.path.join(PROJECT_ROOT, 'repos')
    DEFAULT_OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'Categorizer', 'results')
    
    # Categorizer paths
    CATEGORIZER_PATH = os.path.join(PROJECT_ROOT, 'Categorizer')
    EXEC_ANALYSIS_PATH = os.path.join(CATEGORIZER_PATH, 'src', 'exec_analysis.py')
    
    # Cloner settings
    CLONER_PATH = os.path.join(PROJECT_ROOT, 'cloner', 'cloner.py')
    
    # Session settings
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # CORS settings (if needed for frontend development)
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000']
    
    # Logging
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False
    # In production, SECRET_KEY must be set via environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    def __init__(self):
        super().__init__()
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY environment variable must be set in production")


class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DEBUG = True
    # Use temporary directory for uploads during testing
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'test_uploads')


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """Get configuration based on environment"""
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
