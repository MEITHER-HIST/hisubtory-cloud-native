import pymysql
import sys

# RDS Connection info
DB_CONFIG = {
    'host': 'hisubtory-db.cviagkyaooln.ap-northeast-2.rds.amazonaws.com',
    'user': 'admin',
    'password': '8gEEJTwfFTMRhRFIMNrF',
    'port': 3306,
    'charset': 'utf8mb4'
}

def create_database():
    print("Attempting to create database 'hisubtory_db' on RDS...")
    try:
        # Connect to MySQL (without specific DB)
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS hisubtory_db;")
        print("Success: Database 'hisubtory_db' created or already exists.")
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_database()
