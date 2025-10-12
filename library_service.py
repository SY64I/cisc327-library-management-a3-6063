"""
Library Service Module - Business Logic Functions
Contains all the core business logic for the Library Management System
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import (
    get_book_by_id, get_book_by_isbn, get_patron_borrow_count,
    insert_book, insert_borrow_record, update_book_availability,
    update_borrow_record_return_date, get_all_books, get_patron_borrowed_books,
    get_patron_full_borrow_record
)


def add_book_to_catalog(title: str, author: str, isbn: str, total_copies: int) -> Tuple[bool, str]:
    """
    Add a new book to the catalog.
    Implements R1: Book Catalog Management
    
    Args:
        title: Book title (max 200 chars)
        author: Book author (max 100 chars)
        isbn: 13-digit ISBN
        total_copies: Number of copies (positive integer)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Input validation
    if not title or not title.strip():
        return False, "Title is required."
    
    if len(title.strip()) > 200:
        return False, "Title must be less than 200 characters."
    
    if not author or not author.strip():
        return False, "Author is required."
    
    if len(author.strip()) > 100:
        return False, "Author must be less than 100 characters."
    
    if len(isbn) != 13:
        return False, "ISBN must be exactly 13 digits."
    
    if isbn.isdigit() == False:
        return False, "ISBN must consist of only digits."
    
    if not isinstance(total_copies, int) or total_copies <= 0:
        return False, "Total copies must be a positive integer."
    
    # Check for duplicate ISBN
    existing = get_book_by_isbn(isbn)
    if existing:
        return False, "A book with this ISBN already exists."
    
    # Insert new book
    success = insert_book(title.strip(), author.strip(), isbn, total_copies, total_copies)
    if success:
        return True, f'Book "{title.strip()}" has been successfully added to the catalog.'
    else:
        return False, "Database error occurred while adding the book."

def borrow_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Allow a patron to borrow a book.
    Implements R3 as per requirements  
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists and is available
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    if book['available_copies'] <= 0:
        return False, "This book is currently not available."

    # Check the patron's borrowed books to ensure the book is currently borrowed
    borrowed_books = get_patron_borrowed_books(patron_id)
    
    book_borrowed = False
    for record in borrowed_books:
        if book_id == record['book_id']:
            book_borrowed = True
            break
    
    if book_borrowed:
        return False, "Book is already borrowed."
    
    # Check patron's current borrowed books count
    current_borrowed = get_patron_borrow_count(patron_id)
    
    if current_borrowed >= 5:
        return False, "You have reached the maximum borrowing limit of 5 books."
    
    # Create borrow record
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)
    
    # Insert borrow record and update availability
    borrow_success = insert_borrow_record(patron_id, book_id, borrow_date, due_date)
    if not borrow_success:
        return False, "Database error occurred while creating borrow record."
    
    availability_success = update_book_availability(book_id, -1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."
    
    return True, f'Successfully borrowed "{book["title"]}". Due date: {due_date.strftime("%Y-%m-%d")}.'

def return_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Process book return by a patron.
    
    TODO: Implement R4 as per requirements

    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        tuple: (success: bool, message: str)
    """
     # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    # Check the patron's borrowed books to ensure the book is currently borrowed
    borrowed_books = get_patron_borrowed_books(patron_id)

    book_borrowed = False
    for record in borrowed_books:
        if book_id == record['book_id']:
            book_borrowed = True
            break
    
    if not book_borrowed:
        return False, "Book is not borrowed."
    
    # Update return_date in borrow record
    return_date = datetime.now()

    # Note: update_borrow_record_return_date will set the book's return date to a non-null value, signifying its been returned.
    return_success = update_borrow_record_return_date(patron_id, book_id, return_date)
    if not return_success:
        return False, "Database error occurred while updating return date."
    
    # Update availability
    availability_success = update_book_availability(book_id, 1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."

    return True, f'Successfully returned "{book["title"]}". Return date: {return_date.strftime("%Y-%m-%d")}.'

def calculate_late_fee_for_book(patron_id: str, book_id: int) -> Dict:
    """
    Calculate late fees for a specific book.
    
    TODO: Implement R5 as per requirements 

    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        dict: { fee_amount : int, days_overdue : int, status : str }
    
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return { # return the calculated values
        'fee_amount': -1,
        'days_overdue': -1,
        'status': 'Invalid patron ID. Must be exactly 6 digits.'
    }
    
    # Check if book exists
    book = get_book_by_id(book_id)
    if not book:
        return { # return the calculated values
        'fee_amount': -1,
        'days_overdue': -1,
        'status': 'Book not found.'
    }

    '''
    Plan to calculations:
    Get the patron's borrow records, see if the book exists in the records (kinda like return)
    Take the borrow date, due date, and return date first. If the return date doesnt exist, THEN use the current day instead.
    If the return date exists and is lower than the due date, return 0 fees
    If the return date doesnt exist but the current day is lower than the due date, return 0 fees
    Otherwise, do the calculations as specified using either return date or current day, then return values
    '''

    # Check the patron's full borrow record to ensure the book is or was borrowed
    borrowed_books = get_patron_full_borrow_record(patron_id)

    book_borrowed = False
    book_borrow_record = None
    for record in borrowed_books:
        if book_id == record['book_id']:
            book_borrowed = True
            book_borrow_record = record
            break
    
    if not book_borrowed:
        return { # no calculation is needed
            'fee_amount': -1,
            'days_overdue': -1,
            'status': "Book is not borrowed."
        }

    end_date = datetime.now()
    if book_borrow_record['return_date'] != None:
        end_date = book_borrow_record['return_date']

    if end_date <= book_borrow_record['due_date']: 
        return { # no calculation is needed
            'fee_amount': 0.00,
            'days_overdue': 0,
            'status': "Succesfully calculated, book is not overdue."
        }

    else: 
        fee = 0
        days_late = (end_date - book_borrow_record['due_date']).days
        if days_late > 7: 
            fee = 0.5 * 7
            fee += 1.0 * (days_late - 7)
        
        else: 
            fee = 0.5 * days_late
        
    
    if fee > 15.0:
        fee = 15.0

    return { # return the calculated values
        'fee_amount': fee,
        'days_overdue': days_late,
        'status': "Successfully calculated, book is overdue"
    }
    

def search_books_in_catalog(search_term: str, search_type: str) -> List[Dict]:
    """
    Search for books in the catalog.
    
    TODO: Implement R6 as per requirements
    """

    '''
    Ensure the correct search type is used, otherwise return an error

    Get all books, check for an error

    Look through the resulting list and do the following:
    - Look for partial matching titles (starting with)
    - Look for partial matching authors (starting wtih)
    - Look for exact matching ISBNs

    Return a list of results

    Args:
        search_term: Sequence of characters to match
        search_type: Search type to use (should only be 'title', 'author' or 'ibn')
        
    Returns:
        List[dict], where dict objects are books that are found through search.
    
    '''

    # Check search type
    if not (search_type == 'title' or search_type == 'author' or search_type == 'isbn'):
        return []
    
    books = get_all_books() 
    search_results = []

    # Do search
    for book in books:
        if search_type == 'title':
            if book['title'].lower().startswith(search_term.lower()):
                search_results.append(book)
        if search_type == 'author':
            if book['author'].lower().startswith(search_term.lower()):
                search_results.append(book)
        if search_type == 'isbn':
            if book['isbn'] == search_term:
                search_results.append(book)
            

    return search_results

def get_patron_status_report(patron_id: str) -> Dict:
    """
    Get status report for a patron.
    
    TODO: Implement R7 as per requirements

    Args:
        patron_id: 6-digit library card ID
        
    Returns:
        dict = {book_n_id : book_details, book_(n-1)_id : book_details, ... book_1_id : book_details, books_borrowed : int, total_fee : int }

    where book_details is a full borrow record returned from get_patron_full_borrow_record in database.py.

    """

    '''
    Ensure ISBN is legal
    Retrieve full patron report
    Initialize a dict object to have a count of 0, a fee of 0, and no books
    Iterate through to increment count, to total up owed fees, and append all books
    Return dict
    '''

    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return {}

    # Get the patron's full borrow record
    borrow_records = get_patron_full_borrow_record(patron_id)

    patron_report = {'books_borrowed': get_patron_borrow_count(patron_id), 'total_fee': 0}

    book_num = 1
    for record in borrow_records:
        patron_report['total_fee'] += calculate_late_fee_for_book(patron_id, record['book_id'])['fee_amount']
        title = f'book_{book_num}'
        patron_report[title] = record
        book_num += 1

    return patron_report
