from flask import Blueprint, request, jsonify
from database import get_user_rewards, update_user_rewards

rewards_bp = Blueprint("rewards", __name__)

@rewards_bp.route("/rewards/<int:user_id>", methods=["GET"])
def get_rewards(user_id):
    """Retrieve the user's reward points."""
    points = get_user_rewards(user_id)
    return jsonify({"user_id": user_id, "reward_points": points})

@rewards_bp.route("/rewards/update", methods=["POST"])
def update_rewards():
    """Update reward points based on user transactions."""
    data = request.get_json()
    user_id = data.get("user_id")
    points = data.get("points", 0)

    if not user_id or points <= 0:
        return jsonify({"error": "Invalid data"}), 400

    update_user_rewards(user_id, points)
    return jsonify({"message": "Reward points updated successfully"})
