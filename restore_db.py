import pymysql
import os
import sqlparse

# Database connection details (use env vars if available, otherwise fallback to known RDS)
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'user': os.getenv('DB_USER', 'admin'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'hisubtory_db'),
    'port': int(os.getenv('DB_PORT', 3307)),
    'charset': 'utf8mb4'
}

def restore():
    print("Starting database restore from restore.sql...")
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Read the SQL file
        with open('restore.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Use sqlparse to split the SQL content into individual statements
        statements = sqlparse.split(sql_content)
        
        count = 0
        for statement in statements:
            stmt = statement.strip()
            if not stmt:
                continue
            try:
                cursor.execute(stmt)
                count += 1
            except Exception as e:
                # Log the error but continue with other statements
                print(f"Warning: Failed to execute statement (skipping): {stmt[:100]}... Error: {e}")
        
        conn.commit()
        print(f"Successfully executed {count} statements.")
        conn.close()
    except Exception as e:
        print(f"Error during restore: {e}")

if __name__ == "__main__":
    restore()
