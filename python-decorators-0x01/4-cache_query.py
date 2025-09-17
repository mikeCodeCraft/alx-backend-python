import time
import sqlite3
import functools
from datetime import datetime

query_cache = {}

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

# Create a decorator function called cache_query
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query", None) or (args[0] if args else None)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if query in query_cache:
            print(f"[{timestamp}] Returning cached result for query: {query}")
            return query_cache[query]
        else:
            result = func(*args, **kwargs)
            query_cache[query] = result
            print(f"[{timestamp}] Caching result for query: {query}")
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### Fetch call with cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result 

users_again = fetch_users_with_cache(query="SELECT * FROM users")