import pytest
from services.library_service import (
    add_book_to_catalog, borrow_book_by_patron, return_book_by_patron
)
from database import get_book_id_by_isbn
'''
This script is designed to test for R4, mainly testing the library_service.py return_book_by_patron function.
Make sure to run 'python3 resetdata.py' in the terminal before running 'pytest' so tests run correctly.

Note: These tests assume that the add_book_to_catalog and borrow_book_by_parton functions work as intended.
All the tests below can fail if add_book_to_catalog or borrow_book_by_parton don't work properly.

'''

def test_return_book_valid_input():
    """Test returning a book with valid input."""

    # First add a book
    s_1, m_1 = add_book_to_catalog("Return Me!", "T. Giver", "3456789012345", 3)
    assert s_1 == True

    # Get the book's id, and then borrow it
    book_id = get_book_id_by_isbn("3456789012345")
    s_2, m_2 = borrow_book_by_patron("234567", book_id)
    assert s_2 == True

    # Then, try to return the book
    success, message = return_book_by_patron("234567", book_id)

    assert success == True
    assert "successfully returned" in message.lower()

def test_return_book_invalid_book_id():
    """Test returning a book with an invalid ID"""
    # Note: This test could fail if a book with an id of 0 does exist, which will make the function say the parton does not have the book borrowed instead.

    # Set the book's id to 0
    book_id = 0
    
    # Try returning a 'non-existent' book
    success, message = return_book_by_patron("111111", book_id)

    assert success == False
    assert "not found" in message.lower()

def test_return_book_invalid_patron():
    """Test borrowing a book with an invalid patron ID."""

    # First add a book (this is to ensure a book to return does exist)
    s_1, m_1 = add_book_to_catalog("How To Spot Identity Fraud, 2nd Edition", "I.M. Poster", "0000000002222", 6)
    assert s_1 == True

    # Get the book's id
    book_id = get_book_id_by_isbn("0000000002222")
    # Try to return a book with an invalid patron ID.
    success, message = return_book_by_patron("96", book_id)

    assert success == False
    assert "patron id" in message.lower()

def test_return_book_invalid_not_borrowed():
    """Test returning a book while the patron hasn't borrowed it."""

    # First add a book (to ensure it exists)
    s_1, m_1 = add_book_to_catalog("Forgetful Minds", "Am. Neesha", "1111111000000", 4)
    assert s_1 == True

    # Get the book's id
    book_id = get_book_id_by_isbn("1111111000000")
    # Then, try to return the book without borrowing it
    success, message = return_book_by_patron("246810", book_id)

    assert success == False
    assert "not borrowed" in message.lower()
