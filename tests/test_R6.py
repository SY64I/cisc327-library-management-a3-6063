import pytest
from services.library_service import (
    add_book_to_catalog, search_books_in_catalog
)
from database import get_book_id_by_isbn
'''
This script is designed to test for R6, mainly testing the library_service.py search_books_in_catalog function.

'''

def test_search_valid_title(mocker):
    """Test searching a book with valid title input."""

    test_book = { 'title' : "What were they called, Primogems?"}

    mocker.patch('services.library_service.get_all_books', return_value = [test_book])

    # Then, try to find the book. (titles should be case-insensitve and can be paritally matched)
    results = search_books_in_catalog("what Were They called,", "title")

    # To verify the search results, do a linear search for the item
    found = False
    for d in results:
        if (d["title"] == "What were they called, Primogems?"):
            found = True
            break
    
    assert found

def test_search_valid_author(mocker):
    """Test searching a book with valid author input."""

    test_book = {'author' : "M.E"}

    mocker.patch('services.library_service.get_all_books', return_value = [test_book])

    # Then, try to find the book. (authors should be case-insensitve and can be paritally matched)
    results = search_books_in_catalog("m.", "author")

    # To verify the search results, do a linear search for the item
    found = False
    for d in results:
        if (d["author"] == "M.E"):
            found = True
            break
    
    assert found

def test_search_valid_isbn(mocker):
    """Test searching a book with valid isbn input."""

    test_book = {'isbn' : "7777777777777"}

    mocker.patch('services.library_service.get_all_books', return_value = [test_book])

    # Then, try to find the book. (isbns should be exact matched)
    results = search_books_in_catalog("7777777777777", "isbn")

    # To verify the search results, do a linear search for the item
    found = False
    for d in results:
        if (d["isbn"] == "7777777777777"):
            found = True
            break
    
    assert found

def test_search_invalid_isbn(mocker):
    """Test searching a book with valid isbn input."""

    test_book = {'isbn' : "6868686868686"}

    mocker.patch('services.library_service.get_all_books', return_value = [test_book])

    # Then, try to find the book. (isbns should be exact matched, so this shouldnt work)
    results = search_books_in_catalog("68", "isbn")

    found = False
    for d in results:
        if (d["isbn"] == "6868686868686"):
            found = True
            break
    
    assert not found

def test_search_invalid_search():
    """Test searching a book with invalid search type."""

    # Then, try to find the book by copies. (which shouldn't work)
    results = search_books_in_catalog("45", "copies")

    found = False
    for d in results:
        if (d["isbn"] == "4566544566544"):
            found = True
            break
    
    assert not found






