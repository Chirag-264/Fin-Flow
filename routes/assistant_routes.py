from flask import Blueprint, request, jsonify, session
from database.database import get_db_connection
from ml.ml_model import ai_assistant_response

assistant_routes = Blueprint('assistant_routes', __name__)

# AI Assistant Response
@assistant_routes.route('/assistant', methods=['POST'])
def assistant():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    user_query = data.get('query')

    if not user_query:
        return jsonify({'error': 'Query is required'}), 400

    response = ai_assistant_response(user_query)
    return jsonify({'response': response}), 200
