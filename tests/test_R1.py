import pytest
from services.library_service import (
    add_book_to_catalog
)
'''
This script is designed to test for R1, mainly testing the library_service.py add_book_to_catalog function.
'''
def test_add_valid_input(mocker):
    """Test adding a book with valid input."""
    # Note: This function can fail if a book with the same ID has already been added (like I did when testing myself)

    mocker.patch('services.library_service.get_book_by_isbn', return_value = None)
    mocker.patch('services.library_service.insert_book', return_value = True)
    success, message = add_book_to_catalog("Cataloging for Success", "Mr Success", "1234567890123", 5)
    
    assert success == True
    assert "successfully added" in message.lower()

def test_add_invalid_no_title():
    """Test adding a book with no title."""
    success, message = add_book_to_catalog("", "Uhn Tightuled", "1212121212121", 1)
    
    assert success == False
    assert "Title" in message

def test_add_invalid_title_too_long():
    """Test adding a book with a title that's too long."""
    success, message = add_book_to_catalog("When I was playing Five Nights at Freddy's with my friends, I died to Bonnie on Night 2. Although I was tracking him, I momentarily lost track because I decided to check Foxy as I was under the momentary disposition that his timer was about elapse. Under normal circumstances, this would incite Foxy to transition to his next attack phase, which for context, he was currently in the 3rd of his 5 attack phases. I sincerely believed that if I were to ignore him any longer, I would be forced to camera stall him. However, I did not desire this, as Freddy was nearing my office from the right hallway, meaning that I would have to use my camera stall on Foxy. Ultimately, I had to check camera 7, otherwise known as Pirate's Cove, giving Bonnie the chance to sneak into my office. I was unaware of this, as there was no audio or visual indicator. I then moved to check on Freddy, showing my great hubris in the moment, as in my overestimate of my gamer god skills, I had underestimated the four threats that faced me. In the moment I flipped up my camera, I was shocked and appalled to find that Bonnie had once again seized my run, with the rapid snapping of lagomorphic jaws, fueled by nothing but a steel cold heart and the spirits that came before him. That was the move that made LeBron James cry.", "W. Afton", "3952481987320", 7)
    
    assert success == False
    assert "Title must be less" in message

def test_add_invalid_no_author():
    """Test adding a book with no author."""
    success, message = add_book_to_catalog("Taking Credit For Your Own Work", "", "9498052834576", 1)
    
    assert success == False
    assert "Author" in message

def test_add_invalid_author_too_long():
    """Test adding a book with an author that's too long."""
    success, message = add_book_to_catalog("Guinness World Records: Longest Personal Name", "Adolph Blaine Charles David Earl Frederick Gerald Hubert Irvin John Kenneth Lloyd Martin Nero Oliver Paul Quincy Randolph Sherman Thomas Uncas Victor William Xerxes Yancy Zeus Wolfstern", "6665855901019", 7)
    
    assert success == False
    assert "Author must be less" in message

def test_add_invalid_isbn_length():
    """Test adding a book with an invalid ISBN length."""
    success, message = add_book_to_catalog("The Study of Longevity", "Two Shoret", "154", 3)
    
    assert success == False
    assert "exactly 13 digits" in message


def test_add_invalid_isbn_not_digits():
    """Test adding a book with ISBN with other characters that aren't digits."""
    success, message = add_book_to_catalog("The Study of Digitology", "Ownley Careicters", "ThisWillFail!", 3)
    
    assert success == False
    assert "only digits" in message

def test_add_invalid_negative_copies():
    """Test adding a book with a negative value of total copies."""
    success, message = add_book_to_catalog("Escaping Debt for Dummies", "Noto Posehtifve", "6306913773459", -8)
    
    assert success == False
    assert "positive integer" in message

def test_add_invalid_existing_isbn(mocker):
    """Test adding a book with an isbn of another book"""
    # Note Technically add_book_to_catalog only verfies if a book exists, so I can specify whatever fake book values I want here as long as something exists.
    mocker.patch('services.library_service.get_book_by_isbn', return_value = {'title' : 'This already exists.', 'isbn' : "7899877899878"})

    success, message = add_book_to_catalog("What do you mean this already exists?", "El. Sword", "7899877899878", 3)
    
    assert success == False
    assert "ISBN already exists" in message

def test_add_invalid_database_error(mocker):
    """Test adding a book while encountering a database error."""

    mocker.patch('services.library_service.get_book_by_isbn', return_value = None)
    mocker.patch('services.library_service.insert_book', return_value = False)

    success, message = add_book_to_catalog("Networking Hacks", "Compsigh StuDent", "6758475671567", 4)
    
    assert success == False
    assert "Database error" in message











