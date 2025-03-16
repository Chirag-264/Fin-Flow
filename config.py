import os

class Config:
    """Base configuration with default settings."""
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")  # Change for production
    
    # Database Configuration
    DB_CONFIG = {
        "user": os.getenv("DB_USER", "your_user"),
        "password": os.getenv("DB_PASSWORD", "your_password"),
        "host": os.getenv("DB_HOST", "localhost"),
        "database": os.getenv("DB_NAME", "finflow_db")
    }
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

    # Alpha Vantage API Key
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "your_api_key_here")

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
