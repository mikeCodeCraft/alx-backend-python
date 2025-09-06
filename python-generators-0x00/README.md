# Python Generators Project

This project demonstrates the use of Python generators for efficient data processing, including streaming data from a MySQL database and processing CSV files in batches.

## Files Overview

- **seed.py**  
	Initializes the MySQL database and table, and populates it with sample user data from a CSV file.  
	- Connects to MySQL using credentials from environment variables.
	- Creates the `ALX_prodev` database and `user_data` table if they do not exist.
	- Generates a sample `user_data.csv` if missing.
	- Inserts users from the CSV into the database, avoiding duplicates.

- **0-stream_users.py**  
	Streams user records one by one from the MySQL database using a generator function.

- **1-batch_processing.py**  
	Loads users from a CSV file and processes them in batches using generators.  
	- Filters users over the age of 25 in each batch.

- **2-lazy_paginate.py**  
	Implements lazy pagination over users loaded from a CSV file, yielding pages of users as needed.

- **4-stream_ages.py**  
	Streams user ages from the CSV and calculates the average age using a generator, without loading all data into memory.

## Setup

1. **Install dependencies:**
	 ```
	 pip install mysql-connector-python python-dotenv
	 ```

2. **Set up environment variables:**  
	 Create a `.env` file in the project directory with:
	 ```
	 DB_HOST=localhost
	 DB_USER=root
	 DB_PASSWORD=yourpassword
	 DB_NAME=ALX_prodev
	 ```

3. **Run the seed script to set up the database and sample data:**
	 ```
	 python seed.py
	 ```

## Usage

- Run each script individually to see generator-based data processing in action.
- Adjust the batch size or page size in the scripts as needed.

