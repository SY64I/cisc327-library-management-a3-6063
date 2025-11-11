import pytest
from services.library_service import (
    add_book_to_catalog, borrow_book_by_patron, return_book_by_patron
)
from database import get_book_id_by_isbn
'''
This script is designed to test for R4, mainly testing the library_service.py return_book_by_patron function.

'''

def test_return_valid_input(mocker):
    """Test returning a book with valid input."""

    test_book = {'book_id' : 27, 'title' : "Return Me!"}

    mocker.patch('services.library_service.get_book_by_id', return_value = test_book)
    mocker.patch('services.library_service.get_patron_borrowed_books', return_value = [test_book])
    mocker.patch('services.library_service.update_borrow_record_return_date', return_value = True)
    mocker.patch('services.library_service.update_book_availability', return_value = True)

    # Try to return the book
    success, message = return_book_by_patron("234567", test_book['book_id'])

    assert success == True
    assert "successfully returned" in message.lower()

def test_return_invalid_patron():
    """Test borrowing a book with an invalid patron ID."""

    success, message = return_book_by_patron("96", 1)

    assert success == False
    assert "patron id" in message.lower()

def test_return_invalid_book_id(mocker):
    """Test returning a book with an invalid ID"""
    test_book = {'book_id' : 27}
    mocker.patch('services.library_service.get_book_by_id', return_value = None)
    
    # Try returning a 'non-existent' book
    success, message = return_book_by_patron("111111", test_book['book_id'])

    assert success == False
    assert "not found" in message.lower()


def test_return_book_invalid_not_borrowed(mocker):
    """Test returning a book while the patron hasn't borrowed it."""

    test_book = {'book_id' : 27}

    mocker.patch('services.library_service.get_book_by_id', return_value = test_book)
    mocker.patch('services.library_service.get_patron_borrowed_books', return_value = [])

    # Then, try to return the book without borrowing it
    success, message = return_book_by_patron("246810", test_book['book_id'])

    assert success == False
    assert "not borrowed" in message.lower()

def test_return_invalid_record_error(mocker):
    """Test returning a book with a borrow record error."""

    test_book = {'book_id' : 27}

    mocker.patch('services.library_service.get_book_by_id', return_value = test_book)
    mocker.patch('services.library_service.get_patron_borrowed_books', return_value = [test_book])
    mocker.patch('services.library_service.update_borrow_record_return_date', return_value = False)

    # Try to return the book
    success, message = return_book_by_patron("234567", test_book['book_id'])

    assert success == False
    assert "error occurred while updating return date" in message.lower()

def test_return_invalid_availability_error(mocker):
    """Test returning a book with an availability record error."""

    test_book = {'book_id' : 27}

    mocker.patch('services.library_service.get_book_by_id', return_value = test_book)
    mocker.patch('services.library_service.get_patron_borrowed_books', return_value = [test_book])
    mocker.patch('services.library_service.update_borrow_record_return_date', return_value = True)
    mocker.patch('services.library_service.update_book_availability', return_value = False)

    # Try to return the book
    success, message = return_book_by_patron("234567", test_book['book_id'])

    assert success == False
    assert "error occurred while updating book availability" in message.lower()