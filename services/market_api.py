import requests
import os

# Alpha Vantage API Key (Set this in your environment variables)
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "PJI5WL8BSVCMSK6G")
BASE_URL = "https://www.alphavantage.co/query"

def get_stock_price(symbol):
    """
    Fetches real-time stock price data for a given symbol.
    """
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "5min",  # Fetch data every 5 minutes
        "apikey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    try:
        latest_time = list(data["Time Series (5min)"].keys())[0]
        latest_price = data["Time Series (5min)"][latest_time]["1. open"]
        return {"symbol": symbol, "price": float(latest_price), "timestamp": latest_time}
    except KeyError:
        return {"error": "Invalid response. Check API key or symbol."}
