import sqlite3
from datetime import datetime

class ExecuteQuery:
    def __init__(self, query, params=None, db_name='users.db'):
        self.query = query
        self.db_name = db_name
        self.params = params if params is not None else ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        # Open DB connection
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] Executing query: {self.query} with params: {self.params}")

        try:
            # Execute the query
            self.cursor.execute(self.query, self.params)
            self.results = self.cursor.fetchall()
            return self.results
        except Exception as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()
            raise

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is None:
            self.conn.commit()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] Query executed successfully.")
        self.conn.close()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] Database connection closed.")

# Example usage
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    with ExecuteQuery(query, params) as results:
        print("Query Results:", results)