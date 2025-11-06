import pytest
from services.library_service import (
    add_book_to_catalog, search_books_in_catalog
)
from database import get_book_id_by_isbn
'''
This script is designed to test for R6, mainly testing the library_service.py search_books_in_catalog function.
Make sure to run 'python3 resetdata.py' in the terminal before running 'pytest' so tests run correctly.

Note: These tests assume that that the add_book_to_catalog function works as intended.
All the tests below can fail if add_book_to_catalog doesn't work properly.

Note 2: Some tests below may succeed despite search_books_in_catalog not being implemented.
These tests are being treated as safeguards that should still succeed (in being false) once
search_books_in_catalog has been properly implemented.
'''

def test_search_book_valid_title():
    """Test searching a book with valid title input."""

    # First add a book
    s_1, m_1 = add_book_to_catalog("What were they called, Primogems?", "Stel Ar. Jaid", "5678901234567", 20)
    assert s_1 == True

    # Then, try to find the book. (titles should be case-insensitve and can be paritally matched)
    results = search_books_in_catalog("what Were They called,", "title")

    # To verify the search results, do a linear search for the item
    found = False
    for d in results:
        if (d["title"] == "What were they called, Primogems?"):
            found = True
            break
    
    assert found

def test_search_book_valid_author():
    """Test searching a book with valid author input."""

    # First add a book
    s_1, m_1 = add_book_to_catalog("Who wrote this again?", "M.E", "1616161616161", 12)
    assert s_1 == True

    # Then, try to find the book. (authors should be case-insensitve and can be paritally matched)
    results = search_books_in_catalog("m.", "author")

    # To verify the search results, do a linear search for the item
    found = False
    for d in results:
        if (d["author"] == "M.E"):
            found = True
            break
    
    assert found

def test_search_book_valid_isbn():
    """Test searching a book with valid isbn input."""

    # First add a book
    s_1, m_1 = add_book_to_catalog("ISBNs and You", "Is. Bn", "7777777777777", 7)
    assert s_1 == True

    # Then, try to find the book. (isbns should be exact matched)
    results = search_books_in_catalog("7777777777777", "isbn")

    # To verify the search results, do a linear search for the item
    found = False
    for d in results:
        if (d["isbn"] == "7777777777777"):
            found = True
            break
    
    assert found

def test_search_book_invalid_isbn():
    """Test searching a book with valid isbn input."""

    # First add a book
    s_1, m_1 = add_book_to_catalog("ISBNed", "Nb. Si", "6868686868686", 8)
    assert s_1 == True

    # Then, try to find the book. (isbns should be exact matched, so this shouldnt work)
    results = search_books_in_catalog("68", "isbn")

    found = False
    for d in results:
        if (d["isbn"] == "6868686868686"):
            found = True
            break
    
    assert not found

def test_search_book_invalid_search():
    """Test searching a book with invalid search type."""

    # First add a book
    s_1, m_1 = add_book_to_catalog("Linear Search Tips and Tricks", "Wate Whut", "4566544566544", 5)
    assert s_1 == True

    # Then, try to find the book by copies. (which shouldn't work)
    results = search_books_in_catalog("45", "copies")

    found = False
    for d in results:
        if (d["isbn"] == "4566544566544"):
            found = True
            break
    
    assert not found


