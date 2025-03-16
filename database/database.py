import mysql.connector
import os
import requests
import settings

DB_CONFIG = settings.DB_CONFIG
ALPHA_VANTAGE_API_KEY = settings.ALPHA_VANTAGE_API_KEY


# Establish Database Connection
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Initialize Database and Tables
def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # User Registration Table with reward points
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(100),
            date_of_birth DATE,
            reward_points INT DEFAULT 0
        )
    """)
    
    # Transactions Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            amount DECIMAL(10,2) NOT NULL,
            transaction_type ENUM('bill', 'investment', 'budget') NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # Investment Tracking Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS investments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            stock_name VARCHAR(100),
            amount_of_stocks INT,
            amount_of_money DECIMAL(10,2),
            status ENUM('active', 'closed'),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

# Register a new user
def insert_user_registration(username, password_hash, email, full_name, date_of_birth):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (username, password_hash, email, full_name, date_of_birth) 
        VALUES (%s, %s, %s, %s, %s)
    """, (username, password_hash, email, full_name, date_of_birth))
    
    conn.commit()
    cursor.close()
    conn.close()

# Track a transaction
def insert_transaction_details(user_id, amount, transaction_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (user_id, amount, transaction_type) 
        VALUES (%s, %s, %s)
    """, (user_id, amount, transaction_type))
    
    # Reward System: Increase points based on transaction type
    reward_points = 10 if transaction_type == "investment" else 5
    cursor.execute("""
        UPDATE users SET reward_points = reward_points + %s WHERE id = %s
    """, (reward_points, user_id))

    conn.commit()
    cursor.close()
    conn.close()

# Track an investment
def insert_investment_details(user_id, stock_name, amount_of_stocks, amount_of_money, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO investments (user_id, stock_name, amount_of_stocks, amount_of_money, status) 
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, stock_name, amount_of_stocks, amount_of_money, status))

    # Reward System: Investments give more points
    cursor.execute("""
        UPDATE users SET reward_points = reward_points + 20 WHERE id = %s
    """, (user_id,))
    
    conn.commit()
    cursor.close()
    conn.close()

# Fetch Stock Market Data from Alpha Vantage API
def get_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if "Time Series (5min)" in data:
        return data["Time Series (5min)"]
    else:
        return {"error": "Invalid API response"}

# Retrieve reward points for a user
def get_reward_points(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT reward_points FROM users WHERE id = %s", (user_id,))
    points = cursor.fetchone()
    cursor.close()
    conn.close()
    return points[0] if points else 0
