import csv

# Load user data from CSV
def load_users_from_csv(filepath):
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

# Use the CSV data as our "database"
users_db = load_users_from_csv('user_data.csv')

# SQL components
sql_components = ["SELECT * FROM user_data LIMIT", "OFFSET"]

def stream_users_in_batches(batch_size):
    """Generator that fetches rows in batches"""
    offset = 0
    while True:  # Loop 1
        batch = users_db[offset:offset + batch_size]
        if not batch:
            break
        yield batch
        offset += batch_size

def batch_processing(batch_size):
    """Process each batch to filter users over the age of 25"""
    for batch in stream_users_in_batches(batch_size):  # Loop 2
        filtered_users = []
        for user in batch:  # Loop 3
            if int(user['age']) > 25:
                filtered_users.append(user)
        yield filtered_users

# Example usage
if __name__ == "__main__":
    print("Processing users in batches (filtering age > 25):")
    
    batch_count = 0
    for processed_batch in batch_processing(3):
        batch_count += 1
        print(f"\nBatch {batch_count}: Found {len(processed_batch)} users over 25:")
        for user in processed_batch:
            print(f"  {user['name']}, Age: {user['age']}")