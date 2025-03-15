import pymysql
import os
import requests
from config import DB_CONFIG, ALPHA_VANTAGE_API_KEY

# Database Connection Function
def get_connection():
    return pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        cursorclass=pymysql.cursors.DictCursor
    )

# Initialize Database
def initialize_database():
    connection = pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            cursor.execute(f"USE {DB_CONFIG['database']}")

            # User Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_registration (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    full_name VARCHAR(100),
                    date_of_birth DATE,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Transactions Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transaction_details (
                    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    transaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    amount DECIMAL(10, 2) NOT NULL,
                    transaction_type VARCHAR(50) NOT NULL,
                    description TEXT,
                    FOREIGN KEY (user_id) REFERENCES user_registration(user_id) ON DELETE CASCADE
                )
            """)

            # Investment Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS investment_details (
                    investment_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    stock_name VARCHAR(100) NOT NULL,
                    amount_of_stocks INT NOT NULL,
                    amount_of_money DECIMAL(10, 2) NOT NULL,
                    status ENUM('active', 'closed') NOT NULL,
                    buying_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user_registration(user_id) ON DELETE CASCADE
                )
            """)

            # Emergency Fund Transfers
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS emergency_funds (
                    fund_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    amount DECIMAL(10, 2) NOT NULL,
                    reason TEXT NOT NULL,
                    request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
                    FOREIGN KEY (user_id) REFERENCES user_registration(user_id) ON DELETE CASCADE
                )
            """)

        connection.commit()
    finally:
        connection.close()

# User Registration
def insert_user(username, password, email, full_name, date_of_birth):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO user_registration (username, password, email, full_name, date_of_birth)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (username, password, email, full_name, date_of_birth))
        connection.commit()
    finally:
        connection.close()

# Insert Transaction
def insert_transaction(user_id, amount, transaction_type, description=None):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO transaction_details (user_id, amount, transaction_type, description)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (user_id, amount, transaction_type, description))
        connection.commit()
    finally:
        connection.close()

# Insert Investment
def insert_investment(user_id, stock_name, amount_of_stocks, amount_of_money, status="active"):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO investment_details (user_id, stock_name, amount_of_stocks, amount_of_money, status)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (user_id, stock_name, amount_of_stocks, amount_of_money, status))
        connection.commit()
    finally:
        connection.close()

# Emergency Fund Request
def request_emergency_fund(user_id, amount, reason):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO emergency_funds (user_id, amount, reason)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (user_id, amount, reason))
        connection.commit()
    finally:
        connection.close()

# Fetch User Transactions
def get_transactions(user_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM transaction_details WHERE user_id = %s ORDER BY transaction_time DESC"
            cursor.execute(sql, (user_id,))
            return cursor.fetchall()
    finally:
        connection.close()

# Fetch Investments
def get_investments(user_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM investment_details WHERE user_id = %s ORDER BY buying_time DESC"
            cursor.execute(sql, (user_id,))
            return cursor.fetchall()
    finally:
        connection.close()

# Fetch Emergency Fund Requests
def get_emergency_fund_requests(user_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM emergency_funds WHERE user_id = %s ORDER BY request_time DESC"
            cursor.execute(sql, (user_id,))
            return cursor.fetchall()
    finally:
        connection.close()

# Alpha Vantage API for Real-Time Stock Data
def get_stock_price(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url).json()
    
    try:
        latest_time = list(response['Time Series (5min)'].keys())[0]
        price = response['Time Series (5min)'][latest_time]['1. open']
        return float(price)
    except KeyError:
        return None

