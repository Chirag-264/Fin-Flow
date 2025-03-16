import os
import requests
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from io import StringIO

# Get API key from environment variable
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Function to fetch stock data
def fetch_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&datatype=csv"
    response = requests.get(url)
    
    if response.status_code == 200:
        df = pd.read_csv(StringIO(response.text))
        df = df.rename(columns={"timestamp": "date", "close": "price"})
        df = df[["date", "price"]].iloc[::-1]  # Reverse to chronological order
        return df
    else:
        return None

# Function to train a simple linear regression model
def train_model(data):
    if data is None or len(data) < 10:
        return None

    data["date"] = pd.to_datetime(data["date"])
    data["days"] = (data["date"] - data["date"].min()).dt.days

    X = np.array(data["days"]).reshape(-1, 1)
    y = np.array(data["price"])

    model = LinearRegression()
    model.fit(X, y)

    return model

# Function to predict stock prices
def predict_stock_price(symbol, days_ahead):
    data = fetch_stock_data(symbol)
    model = train_model(data)

    if model is None:
        return {"error": "Not enough data to make a prediction"}

    last_day = (data["date"].max() - data["date"].min()).days
    future_days = np.array([[last_day + days_ahead]])

    predicted_price = model.predict(future_days)[0]
    return {"symbol": symbol, "predicted_price": round(predicted_price, 2)}

# Example usage
if __name__ == "__main__":
    symbol = "AAPL"  # Example stock symbol
    days_ahead = 5   # Predict 5 days into the future
    prediction = predict_stock_price(symbol, days_ahead)
    print(prediction)
