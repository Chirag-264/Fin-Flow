import numpy as np
import pandas as pd
import mysql.connector
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from config import DB_CONFIG

# Establish Database Connection
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Fetch user transactions for predictions
def fetch_user_transactions(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT amount, created_at FROM transactions WHERE user_id = %s", (user_id,))
    transactions = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return transactions

# Predict Future Expenses using Linear Regression
def predict_future_expenses(user_id, months=3):
    transactions = fetch_user_transactions(user_id)
    
    if not transactions or len(transactions) < 3:
        return "Not enough data for prediction"

    df = pd.DataFrame(transactions)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['days_since'] = (df['created_at'] - df['created_at'].min()).dt.days
    df['amount'] = df['amount'].astype(float)

    X = df[['days_since']].values
    y = df['amount'].values

    model = LinearRegression()
    model.fit(X, y)
    
    future_days = np.array([(df['days_since'].max() + i * 30) for i in range(1, months + 1)]).reshape(-1, 1)
    predictions = model.predict(future_days)

    return {f"Month {i+1}": round(pred, 2) for i, pred in enumerate(predictions)}

# Fetch investment options
def fetch_investment_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT stock_name, amount_of_money FROM investments")
    investments = cursor.fetchall()

    cursor.close()
    conn.close()

    return investments

# Recommend investments using KMeans Clustering
def recommend_investments():
    investments = fetch_investment_data()
    
    if len(investments) < 3:
        return "Not enough data to generate recommendations"

    df = pd.DataFrame(investments)
    df['amount_of_money'] = df['amount_of_money'].astype(float)

    kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(df[['amount_of_money']])

    recommended = df[df['Cluster'] == df['Cluster'].mode()[0]]['stock_name'].tolist()
    return {"Recommended Stocks": recommended}

# AI Assistant Response Logic
def ai_assistant_response(user_input):
    user_input = user_input.lower()

    if "expense prediction" in user_input:
        return "I can predict your future expenses. Please provide your User ID."
    elif "investment recommendation" in user_input:
        return "I can recommend investments based on your transaction history."
    elif "reward points" in user_input:
        return "You can check your reward points in the dashboard."
    else:
        return "I'm still learning! Please ask about expenses, investments, or rewards."
