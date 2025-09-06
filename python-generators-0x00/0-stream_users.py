#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error
import os
def stream_users():
    """Generator function that streams users from database one by one"""
    connection = None
    cursor = None
    
    try:
        # Database connection parameters
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            database=os.getenv('DB_NAME', 'ALX_prodev'),
            password=os.getenv('DB_PASSWORD')
        )
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True, buffered=False)
            
            # Execute query to fetch all users
            query = "SELECT * FROM user_data"
            cursor.execute(query)
            
            # Yield rows one by one
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                yield row
                    
    except Error as e:
        print(f"Database error: {e}")
        
    finally:
        # Clean up resources
        try:
            if cursor:
                # Consume any remaining results to avoid "Unread result found" error
                while cursor.nextset():
                    pass
                cursor.close()
            if connection and connection.is_connected():
                connection.close()
        except Error as cleanup_error:
            print(f"Error during cleanup: {cleanup_error}")