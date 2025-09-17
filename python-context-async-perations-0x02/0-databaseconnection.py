import sqlite3
from datetime import datetime

class DatabaseConnection:
    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # Open db connection
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Database connection established.")
        return self.cursor
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Handle errors
        if exc_type:
            # Rollback in case of error
            self.conn.rollback()
            print(f"[{timestamp}] An error occurred: {exc_value}")
        else:
            # Commit any changes if no error
            self.conn.commit()
            print(f"[{timestamp}] Transaction committed.")

        # Close the connection
        self.conn.close()
        print(f"[{timestamp}] Database connection closed.")

# Example usage
if __name__ == "__main__":
    with DatabaseConnection("users.db") as cursor:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print("Users:",users)