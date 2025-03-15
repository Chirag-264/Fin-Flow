from flask import Blueprint, request, jsonify
from database.database import insert_transaction_details, insert_investment_details, transfer_emergency_fund

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

@finance_bp.route("/emergency-transfer", methods=["POST"])
def emergency_transfer():
    """
    Transfers money from emergency fund to the main bank account
    """
    data = request.get_json()
    user_id = data.get("user_id")
    amount = data.get("amount")

    success, message = transfer_emergency_fund(user_id, amount)
    
    if success:
        return jsonify({"message": "Emergency fund transferred successfully"}), 200
    else:
        return jsonify({"error": message}), 400