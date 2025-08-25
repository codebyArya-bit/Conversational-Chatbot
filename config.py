import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # OpenAI settings
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # Chatbot settings
    MAX_MESSAGE_LENGTH = 500
    MAX_RESPONSE_TOKENS = 300
    CHAT_TEMPERATURE = 0.7
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # FAISS settings
    FAISS_INDEX_PATH = 'faiss_index.bin'
    
    # CSV data file
    FAQ_CSV_PATH = 'ICT Cell Common problems - Hardware issues.csv'
    
    # Rate limiting (requests per minute)
    RATE_LIMIT = 30
    
    # Logging
    LOG_LEVEL = 'INFO'
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    
# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}