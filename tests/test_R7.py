import pytest
from services.library_service import (
    get_patron_status_report, return_book_by_patron
)
from database import (
    get_book_id_by_isbn, borrow_test_late_book
)
from datetime import datetime
'''
This script is designed to test for R7, mainly testing the library_service.py get_patron_status_report function.

Note: get_patron_status_report returns a Dict, but it is not specified what the Dict should consist of.
(edit) I have updated what the report dict should return while implementing the function myself:
reportDict = {'book_n_id': book_details, 'book_(n-1)_id': book_details, ... 'book_1_id': book_details, 'books_borrowed': int, 'total_fee': int, }, 
where book_details is a full borrow record returned from get_patron_full_borrow_record in database.py.

If the function runs into an error, the Dict will stay empty. 


'''
def test_report_valid_no_books(mocker):
    """Test creating valid patron report with no books."""

    mocker.patch('services.library_service.get_patron_full_borrow_record', return_value = [])

    # Get the patron's status report (it's assumed that patron 333333 doesn't have any books borrowed already)
    results = get_patron_status_report('333333')

    # To verify the report, check the book count and total fee
    assert results["books_borrowed"] == 0
    # Total late fee should be 6.50 + 15 = $21.50.
    assert results["total_fee"] == 0

def test_report_valid_one_book(mocker):
    """Test creating valid patron report with one book."""

    book_id = 15
    test_report = { 'book_id' : book_id }

    test_fees = {'fee_amount': 0.5}
    mocker.patch('services.library_service.get_patron_full_borrow_record', return_value = [test_report])
    mocker.patch('services.library_service.get_patron_borrow_count', return_value = 1)
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value = test_fees)

    # Then, get the patron's status report
    results = get_patron_status_report('222222')
    
    # To verify the report , do a linear search for the book borrowed.
    foundbook = False
    # Added this to properly iterate through dict
    for d in results.values():
        if not isinstance(d, dict):
            continue
        # Changed this to look for book_id instead of isbn
        if (d['book_id'] == book_id):
            foundbook = True
            break

    assert foundbook
    assert results["books_borrowed"] == 1

    # Total late fee should be $0.50.
    assert results["total_fee"] == 0.5

def test_report_valid_multiple_books(mocker):
    """Test creating valid patron report with multiple books."""

    book_id_1 = 15
    book_id_2 = 21
    test_report_1 = { 'book_id' : book_id_1 }
    test_report_2 = { 'book_id' : book_id_2 }
    
    test_fees = {'fee_amount': 6.5}
    mocker.patch('services.library_service.get_patron_full_borrow_record', return_value = [test_report_1, test_report_2])
    mocker.patch('services.library_service.get_patron_borrow_count', return_value = 2)
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value = test_fees)

    # Then, get the patron's status report
    results = get_patron_status_report('111111')

    # To verify the report , do a linear search for both books borrowed.
    foundbook1 = False
    foundbook2 = False
    #assert results == book_id_1
    # Added this to properly iterate through dict
    for d in results.values():
        if not isinstance(d, dict):
            continue
        #
        if (d['book_id'] == book_id_1):
            foundbook1 = True
        if (d['book_id'] == book_id_2):
            foundbook2 = True
        if (foundbook1 and foundbook2):
            break

    assert foundbook1
    assert foundbook2
    assert results["books_borrowed"] == 2
    # Total late fee should be $13.00
    assert results["total_fee"] == 13


def test_report_valid_returned_late_book(mocker):
    """Test creating valid patron report with a book thats been returned late."""

    book_id = 15
    test_report = { 'book_id' : book_id, 'return_date' : datetime.now() }

    test_fees = {'fee_amount': 2.0}
    mocker.patch('services.library_service.get_patron_full_borrow_record', return_value = [test_report])
    mocker.patch('services.library_service.get_patron_borrow_count', return_value = 0)
    mocker.patch('services.library_service.calculate_late_fee_for_book', return_value = test_fees)

    # Then, get the patron's status report
    results = get_patron_status_report('444444')
    
    # To verify the report , do a linear search for the book borrowed.
    foundbook = False
    for d in results.values():
        if not isinstance(d, dict):
            continue

        if (d['book_id'] == book_id):
            foundbook = True
            # Verify that the book has a return date
            assert not d['return_date'] == None 
            break

    assert foundbook
    # Verify that the patron should not currently have any books borrowed
    assert results["books_borrowed"] == 0

    # Total late fee should be $2.00 (despite being returned).
    assert results["total_fee"] == 2.0

def test_report_invalid_patron():
    """Test creating patron report with invalid patron id."""

    # Try to get a status report with an invalid patron
    results = get_patron_status_report('0')

    # I'm assuming that this should return nothing
    assert results == {}