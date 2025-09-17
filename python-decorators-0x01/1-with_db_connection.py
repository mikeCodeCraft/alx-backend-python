import sqlite3
import functools
from datetime import datetime

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Establish a database connection
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")        
        try:
            # Pass the cursor to the decorated function
            result = func(conn, *args, **kwargs)
            # Commit any changes if the function executed successfully
            return result
        except Exception as e:
            # Rollback in case of error
            conn.rollback()
            print(f"[{timestamp}] An error occurred: {e}")
        finally:
            # Ensure the connection is closed
            conn.close()
            print(f"[{timestamp}] Database connection closed.")    
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

#### Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)