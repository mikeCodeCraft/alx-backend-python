import csv

# Load user data from CSV
def load_users_from_csv(filepath):
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

# Use the CSV data as our "database"
users_db = load_users_from_csv('user_data.csv')

def stream_user_ages():
    """Generator that yields user ages one by one"""
    for user in users_db:  # Loop 1
        yield int(user['age'])

def calculate_average_age():
    """Calculate average age without loading entire dataset into memory"""
    total_age = 0
    count = 0
    
    for age in stream_user_ages():  # Loop 2
        total_age += age
        count += 1
    
    if count == 0:
        return 0
    
    return total_age / count

# Example usage
if __name__ == "__main__":
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age}")