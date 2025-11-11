import pytest
from services.library_service import (
    add_book_to_catalog, borrow_book_by_patron
)
from database import get_book_id_by_isbn
'''
This script is designed to test for R3, mainly testing the library_service.py borrow_book_by_patron function.
'''

def test_borrow_valid_input(mocker):
    """Test borrowing a book with valid input."""
    # Note: This function can fail if the patron has reached their borrow limit.

    test_book = {'book_id' : 12, 'title' : "Borrow Me!", 'available_copies' : 3}

    # A lot of stubbing is involved here...
    mocker.patch('services.library_service.get_book_by_id', return_value = test_book)
    mocker.patch('services.library_service.get_patron_borrowed_books', return_value = [])
    mocker.patch('services.library_service.get_patron_borrow_count', return_value = 0)
    mocker.patch('services.library_service.insert_borrow_record', return_value = True)
    mocker.patch('services.library_service.update_book_availability', return_value = True)

    # Try to borrow the book
    success, message = borrow_book_by_patron("123456", test_book['book_id'])

    assert success == True
    assert "successfully borrowed" in message.lower()

def test_borrow_invalid_patron():
    """Test borrowing a book with an invalid patron ID."""

    # Try to borrow the book
    success, message = borrow_book_by_patron("69", 10)

    assert success == False
    assert "patron id" in message.lower()

def test_borrow_invalid_book_id(mocker):
    """Test borrowing a book with an invalid ID"""
    # Note: This test could fail if a book with an id of 0 does exist, it is assumed that this shouldn't be true.

    test_book = {'book_id' : 12, 'available_copies' : 3}

    mocker.patch('services.library_service.get_book_by_id', return_value = None)

    # Try to borrow the book
    success, message = borrow_book_by_patron("098765", test_book['book_id'])

    assert success == False
    assert "not found" in message.lower()



def test_borrow_invalid_availability(mocker):
    """Test borrowing a book with no copies left available."""

    test_book = {'book_id' : 12, 'available_copies' : 0}

    mocker.patch('services.library_service.get_book_by_id', return_value = test_book)

    # Then try to borrow the book
    success, message = borrow_book_by_patron("098765", test_book['book_id'])

    assert success == False
    assert "not available" in message.lower()

def test_borrow_invalid_already_borrowed(mocker):
    """Test attempting to borrow a book thats already borrowed"""
    test_book = {'book_id' : 12, 'available_copies' : 3}

    mocker.patch('services.library_service.get_book_by_id', return_value = test_book)
    mocker.patch('services.library_service.get_patron_borrowed_books', return_value = [{'book_id' : 12}])

    # Try to borrow the book
    success, message = borrow_book_by_patron("007007", test_book['book_id'])
    
    assert success == False
    assert "already borrowed" in message.lower()

def test_borrow_invalid_borrow_limit(mocker):
    """Test attempting to borrow more books than the borrow limit should allow"""

    test_book = {'book_id' : 12, 'available_copies' : 3}

    mocker.patch('services.library_service.get_book_by_id', return_value = test_book)
    mocker.patch('services.library_service.get_patron_borrowed_books', return_value = [])
    mocker.patch('services.library_service.get_patron_borrow_count', return_value = 5)

    # Try to borrow the book
    success, message = borrow_book_by_patron("689508", test_book['book_id'])

    assert success == False
    assert "maximum borrowing limit" in message.lower()

def test_borrow_invalid_record_error(mocker):
    """Test borrowing a book when encountering a borrow record error."""

    test_book = {'book_id' : 12, 'available_copies' : 3}

    # A lot of stubbing is involved here...
    mocker.patch('services.library_service.get_book_by_id', return_value = test_book)
    mocker.patch('services.library_service.get_patron_borrowed_books', return_value = [])
    mocker.patch('services.library_service.get_patron_borrow_count', return_value = 0)
    mocker.patch('services.library_service.insert_borrow_record', return_value = False)

    # Try to borrow the book
    success, message = borrow_book_by_patron("659305", test_book['book_id'])

    assert success == False
    assert "error occurred while creating borrow record" in message.lower()

def test_borrow_invalid_availability_error(mocker):
    """Test borrowing a book when encountering an availability error."""

    test_book = {'book_id' : 12, 'available_copies' : 3}

    # A lot of stubbing is involved here...
    mocker.patch('services.library_service.get_book_by_id', return_value = test_book)
    mocker.patch('services.library_service.get_patron_borrowed_books', return_value = [])
    mocker.patch('services.library_service.get_patron_borrow_count', return_value = 0)
    mocker.patch('services.library_service.insert_borrow_record', return_value = True)
    mocker.patch('services.library_service.update_book_availability', return_value = False)

    # Try to borrow the book
    success, message = borrow_book_by_patron("222567", test_book['book_id'])

    assert success == False
    assert "error occurred while updating book availability" in message.lower()
