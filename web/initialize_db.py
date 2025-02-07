import os
import sqlite3

# Ensure database directory exists
DB_PATH = os.getenv("SQLITE_DB_PATH", "./user_data.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Connect to SQLite database (it will be created if it doesn't exist)
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        username TEXT NOT NULL,
        date TEXT NOT NULL,
        weight REAL NOT NULL
    )
""")

# Commit and close
connection.commit()
connection.close()

print("Database initialized successfully!")
