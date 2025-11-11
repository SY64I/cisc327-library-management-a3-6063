import pytest
from services.library_service import (
    calculate_late_fee_for_book
)
from database import (
    get_book_id_by_isbn, borrow_test_late_book
)
from datetime import datetime, timedelta
'''
This script is designed to test for R5, mainly testing the library_service.py calculate_late_fee_for_book function.

'''

def test_late_fee_valid_input(mocker):
    """Test calculating a book's late fee with valid input."""

    # First add a test book that is 10 days late
    days_late = 4
    test_report = { 'book_id' : 15,  'due_date' : (datetime.now() - timedelta(days=days_late)), 'return_date' : datetime.now()}

    mocker.patch('services.library_service.get_book_by_id', return_value = {'book_id' : 15})
    mocker.patch('services.library_service.get_patron_full_borrow_record', return_value = [test_report])

    results = calculate_late_fee_for_book("345678", test_report['book_id'])
    
    # If a book is 10 days late, it's fee should be $2.00.
    assert results['fee_amount'] == 2.0
    assert results['days_overdue'] == 10
    assert 'successfully calculated' in results['status'].lower()

def test_late_fee_valid_max_fee(mocker):
    """Test calculating a book's late fee with valid input, when the book's late fee is the max."""

    # First add a test book that is 20 days late
    days_late = 20
    test_report = { 'book_id' : 15,  'due_date' : (datetime.now() - timedelta(days=days_late)), 'return_date' : None }

    mocker.patch('services.library_service.get_book_by_id', return_value = {'book_id' : 15})
    mocker.patch('services.library_service.get_patron_full_borrow_record', return_value = [test_report])

    # Then, try to calculate the book's late fee
    results = calculate_late_fee_for_book("151515", test_report['book_id'])
    
    # If a book is 20 days late, it's fee should be limited to $15 (its calculated cost should be initally above that limit).
    assert results['fee_amount'] == 15
    assert results['days_overdue'] == 20
    assert 'successfully calculated' in results['status'].lower()

def test_late_fee_valid_not_overdue(mocker):
    """Test calculating a book's late fee with a book that isn't overdue"""

    # First add a test book that is 1 day from being late
    test_report = { 'book_id' : 15,  'due_date' : (datetime.now() + timedelta(days=1)), 'return_date' : None }

    mocker.patch('services.library_service.get_book_by_id', return_value = {'book_id' : 15})
    mocker.patch('services.library_service.get_patron_full_borrow_record', return_value = [test_report])

    results = calculate_late_fee_for_book("345678", test_report['book_id'])
    
    # If a book is not overdue, it's fee should be $0.00.
    assert results['fee_amount'] == 0.00
    assert results['days_overdue'] == 0
    assert 'not overdue' in results['status'].lower()

def test_late_fee_invalid_patron():
    """Test calculating a book's late fee with an invalid patron id."""

    test_report = {'book_id' : 27}

    results = calculate_late_fee_for_book("6969", test_report['book_id'])
    
    # This should return 'false' 
    assert results['fee_amount'] == -1
    assert results['days_overdue'] == -1
    assert 'patron id' in results['status'].lower()

def test_late_fee_invalid_book_id(mocker):
    """Test calculating a book's late fee with invalid book id."""

    test_report = { 'book_id' : 15}

    mocker.patch('services.library_service.get_book_by_id', return_value = None)

    # Then, try to calculate the book's late fee without an id
    results = calculate_late_fee_for_book("345678", test_report['book_id'])

    # This should return 'false' (see note at top to understand how I'm currently handling this)
    assert results['fee_amount'] == -1
    assert results['days_overdue'] == -1
    assert 'not found' in results['status'].lower()

def test_late_fee_invalid_not_borrowed(mocker):
    """Test calculating a book's late fee with a book thats not borrowed"""

    test_report = { 'book_id' : 15 }

    mocker.patch('services.library_service.get_book_by_id', return_value = {'book_id' : 15})
    mocker.patch('services.library_service.get_patron_full_borrow_record', return_value = [])

    # Then, try to calculate the book's late fee
    results = calculate_late_fee_for_book("151515", test_report['book_id'])
    
    # If a book is 20 days late, it's fee should be limited to $15 (its calculated cost should be initally above that limit).
    assert results['fee_amount'] == -1
    assert results['days_overdue'] == -1
    assert 'not borrowed' in results['status'].lower()







