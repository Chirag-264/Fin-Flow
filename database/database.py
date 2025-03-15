import pymysql

# Database connection
connection = pymysql.connect(
    host='localhost',
    user='your_username',
    password='your_password'
)

try:
    with connection.cursor() as cursor:
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS finance")
        cursor.execute("USE finance")
        
        # Create user registration details table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_registration (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                password VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                full_name VARCHAR(100),
                date_of_birth DATE,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create transaction details table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transaction_details (
                transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                transaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                amount DECIMAL(10, 2) NOT NULL,
                transaction_type VARCHAR(50) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user_registration(user_id)
            )
        """)
        
        # Create investment details table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS investment_details (
                investment_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                stock_name VARCHAR(100) NOT NULL,
                amount_of_stocks INT NOT NULL,
                amount_of_money DECIMAL(10, 2) NOT NULL,
                status VARCHAR(50) NOT NULL,
                buying_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_registration(user_id)
            )
        """)
        
    connection.commit()
finally:
    connection.close()


def insert_user_registration(username, password, email, full_name, date_of_birth):
        connection = pymysql.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='finance'
        )
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

def insert_transaction_details(user_id, amount, transaction_type):
        connection = pymysql.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='finance'
        )
        try:
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO transaction_details (user_id, amount, transaction_type)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (user_id, amount, transaction_type))
            connection.commit()
        finally:
            connection.close()

def insert_investment_details(user_id, stock_name, amount_of_stocks, amount_of_money, status):
        connection = pymysql.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='finance'
        )
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
