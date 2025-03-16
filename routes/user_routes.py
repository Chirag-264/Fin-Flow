from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.database import get_db_connection

user_routes = Blueprint('user_routes', __name__)

# User Registration
@user_routes.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, email, password, reward_points) VALUES (%s, %s, %s, %s)",
                       (username, email, hashed_password, 0))
        conn.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': 'User already exists or invalid data'}), 400
    finally:
        cursor.close()
        conn.close()

# User Login
@user_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({'message': 'Login successful', 'user': {'id': user['id'], 'username': user['username']}}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# User Logout
@user_routes.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

# Fetch User Profile
@user_routes.route('/profile', methods=['GET'])
def get_profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session['user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT id, username, email, reward_points FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if user:
        return jsonify({'user': user}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

