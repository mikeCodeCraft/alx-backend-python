import mysql.connector
import csv
import uuid
import os
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def connect_db():
    """
    Connects to the MySQL database server
    Returns: connection object or None if failed
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD')
        )
        if connection.is_connected():
            print("Successfully connected to MySQL server")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully (or already exists)")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")

def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL
    Returns: connection object or None if failed
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME', 'ALX_prodev')
        )
        if connection.is_connected():
            print("Successfully connected to ALX_prodev database")
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None

def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields
    """
    try:
        cursor = connection.cursor()
        
        # Create table with proper MySQL syntax
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age INT NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        
        cursor.execute(create_table_query)
        print("Table user_data created successfully")
        cursor.close()
        
    except Error as e:
        print(f"Error creating table: {e}")

def create_sample_csv():
    """Create sample CSV file if it doesn't exist"""
    import csv
    import os
    
    if not os.path.exists('user_data.csv'):
        sample_data = [
            ['user_id', 'name', 'email', 'age'],
            ['550e8400-e29b-41d4-a716-446655440001', 'John Smith', 'john.smith@email.com', 28],
            ['550e8400-e29b-41d4-a716-446655440002', 'Sarah Johnson', 'sarah.johnson@gmail.com', 34],
            ['550e8400-e29b-41d4-a716-446655440003', 'Michael Brown', 'm.brown@yahoo.com', 42],
            ['550e8400-e29b-41d4-a716-446655440004', 'Emily Davis', 'emily.davis@hotmail.com', 29],
            ['550e8400-e29b-41d4-a716-446655440005', 'David Wilson', 'david.wilson@outlook.com', 37],
            ['550e8400-e29b-41d4-a716-446655440006','Jessica Miller','jessica.miller@gmail.com',31],
            ['550e8400-e29b-41d4-a716-446655440007','Christopher Garcia','c.garcia@email.com',45],
            ['550e8400-e29b-41d4-a716-446655440008','Amanda Rodriguez','amanda.r@yahoo.com',26],
            ['550e8400-e29b-41d4-a716-446655440009','Matthew Martinez','matt.martinez@gmail.com',39],
            ['550e8400-e29b-41d4-a716-446655440010','Ashley Anderson','ashley.anderson@hotmail.com',33]
        ]
        
        with open('user_data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(sample_data)
        print("Created user_data.csv file")

def insert_data(connection, csv_file):
    """
    Inserts data from CSV file into the database if it does not exist
    """
    print(f"=== Starting insert_data function ===")
    print(f"CSV file: {csv_file}")
    
    # Create CSV if it doesn't exist
    create_sample_csv()
    
    try:
        import csv
        cursor = connection.cursor()
        
        # Read CSV file
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            count = 0
            for row in csv_reader:
                print(f"Processing: {row['name']}")
                
                # Check if user exists
                check_query = "SELECT user_id FROM user_data WHERE user_id = %s"
                cursor.execute(check_query, (row['user_id'],))
                
                if cursor.fetchone() is None:
                    # Insert new user
                    insert_query = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
                    cursor.execute(insert_query, (row['user_id'], row['name'], row['email'], int(row['age'])))
                    count += 1
                    print(f"  Inserted: {row['name']}")
                else:
                    print(f"  Already exists: {row['name']}")
        
        # Commit changes
        connection.commit()
        print(f"Successfully processed {count} users")
        cursor.close()
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()