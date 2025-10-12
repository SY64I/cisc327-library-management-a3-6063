import pytest
from library_service import (
    get_patron_status_report, return_book_by_patron
)
from database import (
    get_book_id_by_isbn, borrow_test_late_book
)
from datetime import datetime
'''
This script is designed to test for R7, mainly testing the library_service.py get_patron_status_report function.
Make sure to run 'python3 resetdata.py' in the terminal before running 'pytest' so tests run correctly.

Note: get_patron_status_report returns a Dict, but it is not specified what the Dict should consist of.
(edit) I have updated what the report dict should return while implementing the function myself:
reportDict = {'book_n_id': book_details, 'book_(n-1)_id': book_details, ... 'book_1_id': book_details, 'books_borrowed': int, 'total_fee': int, }, 
where book_details is a full borrow record returned from get_patron_full_borrow_record in database.py.

If the function runs into an error, the Dict will stay empty. 

Note 2: The test_patron_report_invalid_patron test case will succeed while get_patron_status_report is 
unimplemented, but exists to be treated as a safeguard that should still succeed (in being false) once
get_patron_status_report has been properly implemented.

Note 3: Note: The test_patron_report_valid_one_returned_late_book() test case
assumes that the return_book_by_patron function works as intended.

'''
def test_patron_report_valid_no_books():
    """Test creating valid patron report with no books."""

    # Get the patron's status report (it's assumed that patron 333333 doesn't have any books borrowed already)
    results = get_patron_status_report('333333')

    # To verify the report, check the book count and total fee
    assert results["books_borrowed"] == 0
    # Total late fee should be 6.50 + 15 = $21.50.
    assert results["total_fee"] == 0

def test_patron_report_valid_one_book():
    """Test creating valid patron report with one book."""

    # First add a test book that is 1 day late
    s_1 = borrow_test_late_book('222222', '0101101011010', 1)
    assert s_1 == True

    # Added this since I changed what my patron_report function returning
    book_id = get_book_id_by_isbn('0101101011010')

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

def test_patron_report_valid_multiple_books():
    """Test creating valid patron report with multiple books."""

    # First add a test book that is 10 days late
    s_1 = borrow_test_late_book('111111', '6789012345678', 10)
    assert s_1 == True
    # Add a second book that is 20 days late
    s_2 = borrow_test_late_book('111111', '7890123456789', 20)
    assert s_2 == True

    # Added this since I changed what my patron_report function returning
    book_id_1 = get_book_id_by_isbn('6789012345678')
    book_id_2 = get_book_id_by_isbn('7890123456789')

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
    # Total late fee should be 6.50 + 15 = $21.50.
    assert results["total_fee"] == 21.5

def test_patron_report_invalid_patron():
    """Test creating patron report with invalid patron id."""

    # Try to get a status report with an invalid patron
    results = get_patron_status_report('0')

    # I'm assuming that this should return nothing
    assert results == {}


def test_patron_report_valid_returned_late_book():
    """Test creating valid patron report with a book thats been returned late."""

    # First add a test book that is 4 days late
    s_1 = borrow_test_late_book('444444', '6483950673291', 4)
    assert s_1 == True

    book_id = get_book_id_by_isbn('6483950673291')

    s_2, m_2 = return_book_by_patron('444444', book_id)
    assert s_2 == True

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