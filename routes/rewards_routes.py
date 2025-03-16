from flask import Blueprint, request, jsonify
from database import get_db_connection
from ml.ml_model import evaluate_financial_discipline

rewards_routes = Blueprint("rewards_routes", __name__)

# Route: Get User Rewards
@rewards_routes.route("/get_rewards", methods=["GET"])
def get_rewards():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT reward_points FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if not result:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user_id": user_id, "reward_points": result[0]})

# Route: Update Rewards Based on AI Analysis
@rewards_routes.route("/update_rewards", methods=["POST"])
def update_rewards():
    data = request.get_json()
    user_id = data.get("user_id")
    
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # AI evaluates spending behavior and assigns reward points
    reward_points = evaluate_financial_discipline(user_id)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET reward_points = reward_points + %s WHERE id = %s", (reward_points, user_id))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Rewards updated successfully", "new_reward_points": reward_points})

# Route: Redeem Rewards
@rewards_routes.route("/redeem_rewards", methods=["POST"])
def redeem_rewards():
    data = request.get_json()
    user_id = data.get("user_id")
    points_to_redeem = data.get("points")

    if not user_id or points_to_redeem is None:
        return jsonify({"error": "User ID and points to redeem are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT reward_points FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()

    if not result or result[0] < points_to_redeem:
        cursor.close()
        conn.close()
        return jsonify({"error": "Not enough reward points"}), 400

    cursor.execute("UPDATE users SET reward_points = reward_points - %s WHERE id = %s", (points_to_redeem, user_id))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Rewards redeemed successfully", "remaining_points": result[0] - points_to_redeem})
