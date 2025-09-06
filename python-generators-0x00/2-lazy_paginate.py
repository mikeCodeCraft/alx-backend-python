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

def paginate_users(page_size, offset):
    return users_db[offset:offset + page_size]

def lazy_paginate(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

# Example usage
if __name__ == "__main__":
    for page in lazy_paginate(10):
        print(f"Fetched {len(page)} users:")
        for user in page:
            print(user)