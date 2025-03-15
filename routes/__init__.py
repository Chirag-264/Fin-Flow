from flask import Flask
from routes.user_routes import user_bp
from routes.finance_routes import finance_bp
from database.database import init_db

def create_app():
    app = Flask(__name__)

    # Initialize database (if needed)
    init_db()

    # Register Blueprints (modular routes)
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(finance_bp, url_prefix="/finance")

    return app
