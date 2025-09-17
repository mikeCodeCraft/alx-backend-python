import time
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

# Create a decorator function called retry_on_failure
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"[{timestamp}] Attempt {attempts} failed: {e}")
                    if attempts < retries:
                        print(f"[{timestamp}] Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print(f"[{timestamp}] All {retries} reached. Operation failed.")
                        raise
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### Fetch users with automatic retry on failure
users = fetch_users_with_retry()

print(users)
