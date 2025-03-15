import mysql.connector

# Database Config
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "yourpassword",
    "database": "finflow"
}

def init_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("Database Connected Successfully!")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database Connection Failed: {e}")
