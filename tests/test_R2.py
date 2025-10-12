import pytest
from library_service import (
    add_book_to_catalog
)

from database import (
    get_all_books, update_book_availability, clear_all_data, get_book_id_by_isbn
)

'''
This script is designed to test for R2, mainly testing the database.py get_all_books function.
Make sure to run 'python3 resetdata.py' in the terminal before running 'pytest' so tests run correctly.

Note: These tests assume that the add_book_to_catalog function works as intended.
Most tests below can fail if add_book_to_catalog doesn't work properly.

'''

def test_book_catalog_valid_list():
    """Test a valid book catalog."""
    # Note: This function can fail if a book with the same ID has already been added 
    s_1, m_1 = add_book_to_catalog("The First Of Many", "No. 1", "1111110111111", 1)
    assert s_1 == True

    s_2, m_2 = add_book_to_catalog("The Second To Come", "No. 2", "2222220222222", 2)
    assert s_2 == True
    
    catalog = get_all_books()

    # To verify the catalog, look at the information given
    foundbook1 = False
    foundbook2 = False
    for b in catalog:
        if (b["title"] == 'The First Of Many' 
        and b["author"] == 'No. 1' 
        and b["isbn"] == '1111110111111'):
            foundbook1 = True
        
        if (b["title"] == 'The Second To Come' 
        and b["author"] == 'No. 2' 
        and b["isbn"] == '2222220222222'):
            foundbook2 = True
        
        if (foundbook1 and foundbook2):
            break

    assert foundbook1
    assert foundbook2

def test_book_catalog_valid_empty_list():
    """Test an empty book catalog."""

    # Clear the database
    clear_all_data()

    catalog = get_all_books()

    # To verify the catalog, check to make sure the catalog is empty
    assert catalog == []

def test_book_catalog_valid_copies():
    """Test checking book total/available copies"""
    # Note: This function can fail if a book with the same ID has already been added 
    s_1, m_1 = add_book_to_catalog("The Third In Line", "No. 3", "3333330333333", 3)
    assert s_1 == True
    
    # Get the book's id
    book_id = get_book_id_by_isbn("3333330333333")

    # Set the book's available copies to 1
    s_2 = update_book_availability(book_id, -2)
    assert s_2 == True

    catalog = get_all_books()

    # To verify the catalog, look at the information given, plus the total/available copies
    valid_copies = False
    for b in catalog:
        if (b["title"] == 'The Third In Line' 
        and b["author"] == 'No. 3' 
        and b["isbn"] == '3333330333333'
        and b["total_copies"] == 3
        and b["available_copies"] == 1):
            valid_copies = True
            break

    assert valid_copies
    
def test_book_catalog_valid_add_remove():
    """Test adding and removing a book from the catalog"""
    # Note: This function can fail if a book with the same ID has already been added 
    s_1, m_1 = add_book_to_catalog("The Fourth On Route", "No. 4", "4444440444444", 4)
    assert s_1 == True

    catalog = get_all_books()

    # See if the book exists in the catalog currently
    book_exists = False
    for b in catalog:
        if (b["isbn"] == '4444440444444'):
            book_exists = True
            break

    assert book_exists

    #Clear the database
    clear_all_data()

    catalog = get_all_books()
    
    # See if the book still exists in the catalog currently
    book_exists = False
    for b in catalog:
        if (b["isbn"] == '4444440444444'):
            book_exists = True
            break

    assert not book_exists