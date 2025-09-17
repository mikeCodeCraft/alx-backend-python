import sqlite3
import functools
from datetime import datetime

# Create a decorator function for db connection
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

# Create a decorator function called transactional
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print(f"[{timestamp}] Transaction committed.")
            return result
        except Exception as e:
            conn.rollback()
            print(f"[{timestamp}] Transaction rolled back due to error: {e}")
            raise
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

#### Update User's email with automatic transaction handling
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')