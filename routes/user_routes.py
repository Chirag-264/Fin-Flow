from flask import Blueprint, request, jsonify, session
from database import get_user_by_email, insert_user_registration, update_user_rewards
from werkzeug.security import generate_password_hash, check_password_hash

user_routes = Blueprint("user_routes", __name__)

# User Registration
@user_routes.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not all(k in data for k in ("username", "email", "password", "full_name", "date_of_birth")):
        return jsonify({"error": "Missing required fields"}), 400

    existing_user = get_user_by_email(data["email"])
    if existing_user:
        return jsonify({"error": "Email already registered"}), 409

    hashed_password = generate_password_hash(data["password"])
    insert_user_registration(
        data["username"],
        hashed_password,
        data["email"],
        data["full_name"],
        data["date_of_birth"],
    )

    return jsonify({"message": "User registered successfully"}), 201

# User Login
@user_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not all(k in data for k in ("email", "password")):
        return jsonify({"error": "Missing email or password"}), 400

    user = get_user_by_email(data["email"])
    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    session["user_id"] = user["id"]
    session["username"] = user["username"]

    return jsonify({"message": "Login successful", "user": {"id": user["id"], "username": user["username"]}}), 200

# User Logout
@user_routes.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

# Get User Info (Authenticated)
@user_routes.route("/user", methods=["GET"])
def get_user():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({"user": {"id": session["user_id"], "username": session["username"]}}), 200

# Reward System API (Fetch User Points)
@user_routes.route("/rewards", methods=["GET"])
def get_rewards():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user = get_user_by_email(session["username"])
    return jsonify({"rewards": user["reward_points"]}), 200

# Update Rewards
@user_routes.route("/update_rewards", methods=["POST"])
def update_rewards():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if "points" not in data:
        return jsonify({"error": "Missing points"}), 400

    update_user_rewards(session["user_id"], data["points"])
    return jsonify({"message": "Rewards updated"}), 200
