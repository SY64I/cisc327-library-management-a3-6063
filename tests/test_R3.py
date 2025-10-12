import pytest
from library_service import (
    add_book_to_catalog, borrow_book_by_patron
)
from database import get_book_id_by_isbn
'''
This script is designed to test for R3, mainly testing the library_service.py borrow_book_by_patron function.
Make sure to run 'python3 resetdata.py' in the terminal before running 'pytest' so tests run correctly.

Note: These tests assume that the add_book_to_catalog function works as intended.
All the tests below can fail if add_book_to_catalog doesn't work properly.

'''

def test_borrow_book_valid_input():
    """Test borrowing a book with valid input."""
    # Note: This function can fail if the patron has reached their borrow limit.

    # First add a book
    s, m = add_book_to_catalog("Borrow Me!", "T. Giver", "2345678901234", 3)
    assert s == True

    # Get the book's id
    book_id = get_book_id_by_isbn("2345678901234")
    # Then try to borrow the book
    success, message = borrow_book_by_patron("123456", book_id)

    assert success == True
    assert "successfully borrowed" in message.lower()

def test_borrow_book_invalid_book_id():
    """Test borrowing a book with an invalid ID"""
    # Note: This test could fail if a book with an id of 0 does exist, it is assumed that this shouldn't be true.

    # Set the book's id to 0
    book_id = 0
    # Then try to borrow the book
    success, message = borrow_book_by_patron("098765", book_id)

    assert success == False
    assert "not found" in message.lower()

def test_borrow_book_invalid_patron():
    """Test borrowing a book with an invalid patron ID."""

    # First add a book
    s, m = add_book_to_catalog("How To Spot Identity Fraud", "I.M. Poster", "0000000001111", 3)
    assert s == True

    # Get the book's id
    book_id = get_book_id_by_isbn("0000000001111")

    # Try to borrow the book without the correct patron ID.
    success, message = borrow_book_by_patron("69", book_id)

    assert success == False
    assert "patron id" in message.lower()

def test_borrow_book_invalid_availability():
    """Test borrowing a book with no copies left available."""

    # First add a book
    s, m = add_book_to_catalog("Singularity, Limited Edition", "Rare Inc.", "0000000000001", 1)
    assert s == True

    # Get the book's id
    book_id = get_book_id_by_isbn("0000000000001")
    
    # Then try to borrow the book 2 times, with only 1 copy of the book existing
    for i in range (1, 6):
        success, message = borrow_book_by_patron("911420", book_id)

    assert success == False
    assert "not available" in message.lower()


def test_borrow_book_invalid_borrow_limit():
    """Test attempting to borrow more books than the borrow limit should allow"""

    
    # First borrow 5 books (should be the borrow limit)
    isbn = 1987654321123
    for i in range (0, 5): 
        s_1, m_2 = add_book_to_catalog("Reworked Requirements", "R. Case", str(isbn), 1)
        assert s_1 == True

        book_id = get_book_id_by_isbn(str(isbn))
        s_2, m_2 = borrow_book_by_patron("689508", book_id)
        assert s_2 == True
        isbn += 1
    
    # Then try to borrow a 6th book (should be invalid)
    s_3, m_3 = add_book_to_catalog("Hoarders Anonymous", "B. Borrow", "0987654321098", 10)
    assert s_3 == True
    book_id_2 = get_book_id_by_isbn("0987654321098")

    success, message = borrow_book_by_patron("689508", book_id_2)
    assert success == False
    assert "maximum borrowing limit" in message.lower()

def test_borrow_book_invalid_already_borrowed():
    """Test attempting to borrow a book thats already borrowed"""

    # First add a book
    s, m = add_book_to_catalog("A Guide to Duplication", "You. Nicque", "0070070070077", 10)
    assert s == True

    book_id = get_book_id_by_isbn("0070070070077")
    # Then try to borrow the book twice
    for i in range (0, 2):
        success, message = borrow_book_by_patron("007007", book_id)
    
    assert success == False
    assert "already borrowed" in message.lower()

