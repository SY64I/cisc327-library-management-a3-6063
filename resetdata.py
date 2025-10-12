from database import init_database, add_sample_data, clear_all_data, get_all_books

# Script designed to call the database.py clear_all_data() function easily for testing.
if __name__ == '__main__':
    init_database()
    clear_all_data()