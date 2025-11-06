import pytest
from services.library_service import (
    calculate_late_fee_for_book
)
from database import (
    get_book_id_by_isbn, borrow_test_late_book
)
from datetime import datetime
'''
This script is designed to test for R5, mainly testing the library_service.py calculate_late_fee_for_book function.
Make sure to run 'python3 resetdata.py' in the terminal before running 'pytest' so tests run correctly.

Note: I'm going to assume for now that if calculate_late_fee_for_book should return 'false', 
'fee_amount' and 'days_overdue' will be set to -1, similar to how a C function's exit status would behave.

'''

def test_late_fee_valid_input():
    """Test calculating a book's late fee with valid input."""

    # First add a test book that is 10 days late
    s_1 = borrow_test_late_book('345678', '4567890123456', 10)
    assert s_1 == True

    # Get the book's id
    book_id = get_book_id_by_isbn("4567890123456")
    # Then, try to calculate the book's late fee
    results = calculate_late_fee_for_book("345678", book_id)
    
    # If a book is 10 days late, it's fee should be $6.50.
    assert results['fee_amount'] == 6.5
    assert results['days_overdue'] == 10
    assert 'successfully calculated' in results['status'].lower()

def test_late_fee_valid_max_fee():
    """Test calculating a book's late fee with valid input, when the book's late fee is the max."""

    # First add a test book that is 20 days late
    s_1 = borrow_test_late_book('151515', '1515151515151', 20)
    assert s_1 == True

    # Get the book's id
    book_id = get_book_id_by_isbn("1515151515151")
    # Then, try to calculate the book's late fee
    results = calculate_late_fee_for_book("151515", book_id)
    
    # If a book is 20 days late, it's fee should be limited to $15 (its calculated cost should be initally above that limit).
    assert results['fee_amount'] == 15
    assert results['days_overdue'] == 20
    assert 'successfully calculated' in results['status'].lower()

def test_late_fee_invalid_book_id():
    """Test calculating a book's late fee with invalid book id."""
    # Note: This test could fail if a book with an id of 0 does exist.

    # Set book id to 0
    book_id = 0
    # Then, try to calculate the book's late fee without an id
    results = calculate_late_fee_for_book("345678", book_id)

    # This should return 'false' (see note at top to understand how I'm currently handling this)
    assert results['fee_amount'] == -1
    assert results['days_overdue'] == -1
    assert 'not found' in results['status'].lower()

def test_late_fee_invalid_patron():
    """Test calculating a book's late fee with an invalid patron id."""

    # First add a test book that is 7 days late
    s_1 = borrow_test_late_book('345678', '0000000003333', 7)
    assert s_1 == True

    # Get the book's id
    book_id = get_book_id_by_isbn("0000000003333")
    # Then, try to calculate the book's late fee
    results = calculate_late_fee_for_book("6969", book_id)
    
    # This should return 'false' 
    assert results['fee_amount'] == -1
    assert results['days_overdue'] == -1
    assert 'patron id' in results['status'].lower()

