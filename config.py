import os

class Config:
    """Base configuration with default settings."""
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")  # Change in production!
    DEBUG = True  # Set to False in production

    # Database Configuration (MySQL)
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "your_username")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
    DB_NAME = os.getenv("DB_NAME", "finance")

    # Flask SQLAlchemy URI (if using SQLAlchemy)
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AI Model Configuration
    MODEL_PATH = os.getenv("MODEL_PATH", "ml_model/savings_predictor.pkl")

    # Other settings
    REWARD_THRESHOLD = 10  # Example: Users must save 10% more to get rewards
    MIN_EMERGENCY_FUNDS = 1000  # Minimum savings before investing

class ProductionConfig(Config):
    """Production-specific configurations."""
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY", "super_secure_production_key")

class DevelopmentConfig(Config):
    """Development-specific configurations."""
    DEBUG = True

class TestingConfig(Config):
    """Testing-specific configurations."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Use in-memory DB for testing

# Choose the right config
config = DevelopmentConfig()

