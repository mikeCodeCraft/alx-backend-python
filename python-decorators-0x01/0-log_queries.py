import sqlite3
import functools
from datetime import datetime


def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT UNIQUE NOT NULL
        );
    """)

    # Populate with sample data
    try:
        cursor.executemany('''
            INSERT INTO users (name, age, email) VALUES (?, ?, ?);
        ''', [
            ('Yusuf', 30, "yusuf@test.com"),
            ('prince', 25, "price@test.com"),
            ('Charlie', 35, "charlie@test.com")
        ])

    except sqlite3.IntegrityError:
        pass  # Ignore if data already exists


    conn.commit()
    conn.close()

# Run db setup
init_db()
print("Database initialized and populated with sample data.")



#### docarotor to lof SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query", None) or (args[0] if args else None)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}]Executing SQL Query: {query}")
        try:
            result = func(*args, **kwargs)
            print(f"[{timestamp}]Query executed successfully.")
            return result
        except Exception as e:
            print(f"[{timestamp}]Error executing query: {e}")
            raise
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users;")