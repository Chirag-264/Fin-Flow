import os

class Config:
    """Base configuration with default settings."""
    SECRET_KEY = os.getenv("SECRET_KEY", "e5b7a9d9f34c6f1a3d2b5c9f8a7e6d1c4b3a2f9e8d7c6b5a1e2d3f4c5b6a7d8e")  # Change for production
    
    # Database Configuration
    DB_CONFIG = {
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "WWzcQRIMSAqDRjhoLxpzSwQYmNYmhkgq"),
        "host": os.getenv("DB_HOST", "mysql.railway.internal"),
        "database": os.getenv("DB_NAME", "railway"),
        "port": os.getenv("MYSQLPORT", 3306)
    }
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

    # Alpha Vantage API Key
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "PJI5WL8BSVCMSK6G")

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
