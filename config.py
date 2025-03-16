import os

class Config:
    """Base configuration with default settings."""
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")  # Change for production
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost/finflow_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production-specific configuration."""
    DEBUG = False

# Set the configuration mode (default to Development)
config_mode = os.getenv("FLASK_ENV", "development")

if config_mode == "production":
    app_config = ProductionConfig()
else:
    app_config = DevelopmentConfig()
