from flask import Blueprint, request, jsonify
from database.database import insert_user_registration

user_bp = Blueprint("user", __name__)

@user_bp.route("/register", methods=["POST"])
def register():
    #API to register a new user.
    data = request.get_json()
    if not all(k in data for k in ("username", "password", "email", "full_name", "date_of_birth")):
        return jsonify({"error": "Missing required fields"}), 400

    insert_user_registration(
        data["username"],
        data["password"],
        data["email"],
        data["full_name"],
        data["date_of_birth"],
    )
    return jsonify({"message": "User registered successfully"}), 201
