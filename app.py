from flask import Flask
from flask_cors import CORS
from config import Config
from database.database import create_tables
from routes.user_routes import user_bp
from routes.finance_routes import finance_bp
from routes.rewards_routes import rewards_bp
from routes.assistant_routes import assistant_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Register Blueprints
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(finance_bp, url_prefix="/finance")
app.register_blueprint(rewards_bp, url_prefix="/rewards")
app.register_blueprint(assistant_bp, url_prefix="/assistant")

# Create database tables before first request
@app.before_first_request
def initialize_database():
    create_tables()

if __name__ == "__main__":
    app.run(debug=True)



