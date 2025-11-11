import pytest
from services.library_service import (
    add_book_to_catalog
)
from database import clear_all_data

def test_add_book_valid_input(mocker):
    """Test adding a book with valid input."""
    """Test adding a book with valid input."""
    # Note: This function can fail if a book with the same ID has already been added (like I did when testing myself)

    mocker.patch('services.library_service.get_book_by_isbn', return_value = None)
    mocker.patch('services.library_service.insert_book', return_value = True)
    success, message = add_book_to_catalog("Cataloging for Success", "Mr Success", "1234567890123", 5)
    
    assert success == True
    assert "successfully added" in message.lower()
    #clear_all_data()

def test_add_book_invalid_isbn_too_short():
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    
    assert success == False
    assert "13 digits" in message



# Add more test methods for each function and edge case. You can keep all your test in a separate folder named `tests`.