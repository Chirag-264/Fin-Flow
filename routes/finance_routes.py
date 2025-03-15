from flask import Blueprint, request, jsonify
from database.database import insert_transaction_details, insert_investment_details

finance_bp = Blueprint("finance", __name__)

@finance_bp.route("/track-transaction", methods=["POST"])
def track_transaction():
    """API to track user transactions (bills, investments, budgeting)."""
    data = request.get_json()
    if not all(k in data for k in ("user_id", "amount", "transaction_type")):
        return jsonify({"error": "Missing required fields"}), 400

    insert_transaction_details(data["user_id"], data["amount"], data["transaction_type"])
    return jsonify({"message": "Transaction recorded successfully"}), 201

@finance_bp.route("/track-investment", methods=["POST"])
def track_investment():
    """API to track user investments with real-time status."""
    data = request.get_json()
    if not all(k in data for k in ("user_id", "stock_name", "amount_of_stocks", "amount_of_money", "status")):
        return jsonify({"error": "Missing required fields"}), 400

    insert_investment_details(
        data["user_id"],
        data["stock_name"],
        data["amount_of_stocks"],
        data["amount_of_money"],
        data["status"],
    )
    return jsonify({"message": "Investment recorded successfully"}), 201
