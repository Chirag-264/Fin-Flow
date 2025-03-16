import requests
from flask import Blueprint, request, jsonify
from database import get_db_connection
from config import ALPHA_VANTAGE_API_KEY
from ml.ml_model import analyze_market_trends

market_routes = Blueprint("market_routes", __name__)

# Route: Fetch Real-Time Stock Price
@market_routes.route("/stock_price", methods=["GET"])
def stock_price():
    symbol = request.args.get("symbol")
    if not symbol:
        return jsonify({"error": "Stock symbol is required"}), 400

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch stock data"}), 500

    data = response.json()
    time_series = data.get("Time Series (5min)", {})

    if not time_series:
        return jsonify({"error": "No stock data available"}), 404

    latest_timestamp = sorted(time_series.keys())[-1]
    latest_price = time_series[latest_timestamp]["1. open"]

    return jsonify({"symbol": symbol, "latest_price": latest_price, "timestamp": latest_timestamp})

# Route: Market Trend Analysis (AI Processing)
@market_routes.route("/market_trends", methods=["GET"])
def market_trends():
    symbol = request.args.get("symbol")
    if not symbol:
        return jsonify({"error": "Stock symbol is required"}), 400

    trends = analyze_market_trends(symbol)
    return jsonify({"market_trends": trends})

# Route: Save Market Data to Database
@market_routes.route("/save_stock_data", methods=["POST"])
def save_stock_data():
    data = request.get_json()
    symbol = data.get("symbol")
    price = data.get("price")

    if not symbol or not price:
        return jsonify({"error": "Symbol and price are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "INSERT INTO stock_data (symbol, price) VALUES (%s, %s)"
    cursor.execute(query, (symbol, price))
    
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Stock data saved successfully"}), 201
