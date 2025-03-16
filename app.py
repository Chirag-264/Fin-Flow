from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
import os
import pymysql
pymysql.install_as_MySQLdb()


# Initialize database
db = SQLAlchemy()

def create_app():
    """Flask application factory."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object("config.app_config")
    
    # Initialize database
    db.init_app(app)
    
    # Enable CORS
    CORS(app)
    
    # Ensure logs directory exists
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Logging setup
    file_handler = RotatingFileHandler("logs/error.log", maxBytes=10240, backupCount=3)
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logging.basicConfig(level=logging.INFO, handlers=[file_handler])
    
    # Register Blueprints (routes)
    from routes.user_routes import user_bp
    from routes.finance_routes import finance_bp
    from routes.market_routes import market_bp
    from routes.rewards_routes import rewards_bp
    from routes.assistant_routes import assistant_bp
    
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(finance_bp, url_prefix="/finance")
    app.register_blueprint(market_bp, url_prefix="/market")
    app.register_blueprint(rewards_bp, url_prefix="/rewards")
    app.register_blueprint(assistant_bp, url_prefix="/assistant")
    
    return app
