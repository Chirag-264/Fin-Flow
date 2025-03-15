from flask import Blueprint, request, jsonify
from services.market_api import get_stock_price

market_bp = Blueprint("market", __name__)

@market_bp.route("/stock-price", methods=["GET"])
def stock_price():
    """
    API endpoint to fetch real-time stock price.
    Example: /stock-price?symbol=AAPL
    """
    symbol = request.args.get("symbol", "").upper()
    if not symbol:
        return jsonify({"error": "Stock symbol is required"}), 400

    result = get_stock_price(symbol)
    return jsonify(result)
