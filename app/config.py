"""Application Configuration"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration"""
    DEBUG = os.getenv("DEBUG", "False") == "True"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    API_TITLE = "Python Application"
    API_VERSION = "1.0.0"


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENVIRONMENT = "development"


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENVIRONMENT = "production"


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    ENVIRONMENT = "testing"
    TESTING = True


def get_config():
    """Get configuration based on environment"""
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()


config = get_config()
