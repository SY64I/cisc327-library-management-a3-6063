import pytest
from services.library_service import (
    add_book_to_catalog
)
'''
This script is designed to test for R1, mainly testing the library_service.py add_book_to_catalog function.
Make sure to run 'python3 resetdata.py' in the terminal before running 'pytest' so tests run correctly.
'''
def test_add_book_valid_input():
    """Test adding a book with valid input."""
    # Note: This function can fail if a book with the same ID has already been added (like I did when testing myself)
    success, message = add_book_to_catalog("Cataloging for Success", "Mr Success", "1234567890123", 5)
    
    assert success == True
    assert "successfully added" in message.lower()

def test_add_book_invalid_copies_not_positive():
    """Test adding a book with a negative value of total copies."""
    success, message = add_book_to_catalog("Escaping Debt for Dummies", "Noto Posehtifve", "6306913773459", -8)
    
    assert success == False
    assert "positive integer" in message

def test_add_book_invalid_no_title():
    """Test adding a book with no title."""
    success, message = add_book_to_catalog("", "Uhn Tightuled", "1212121212121", 1)
    
    assert success == False
    assert "Title" in message

def test_add_book_invalid_no_author():
    """Test adding a book with no author."""
    success, message = add_book_to_catalog("Taking Credit For Your Own Work", "", "9498052834576", 1)
    
    assert success == False
    assert "Author" in message

def test_add_book_invalid_title_too_long():
    """Test adding a book with a title that's too long."""
    success, message = add_book_to_catalog("When I was playing Five Nights at Freddy's with my friends, I died to Bonnie on Night 2. Although I was tracking him, I momentarily lost track because I decided to check Foxy as I was under the momentary disposition that his timer was about elapse. Under normal circumstances, this would incite Foxy to transition to his next attack phase, which for context, he was currently in the 3rd of his 5 attack phases. I sincerely believed that if I were to ignore him any longer, I would be forced to camera stall him. However, I did not desire this, as Freddy was nearing my office from the right hallway, meaning that I would have to use my camera stall on Foxy. Ultimately, I had to check camera 7, otherwise known as Pirate's Cove, giving Bonnie the chance to sneak into my office. I was unaware of this, as there was no audio or visual indicator. I then moved to check on Freddy, showing my great hubris in the moment, as in my overestimate of my gamer god skills, I had underestimated the four threats that faced me. In the moment I flipped up my camera, I was shocked and appalled to find that Bonnie had once again seized my run, with the rapid snapping of lagomorphic jaws, fueled by nothing but a steel cold heart and the spirits that came before him. That was the move that made LeBron James cry.", "W. Afton", "3952481987320", 7)
    
    assert success == False
    assert "Title must be less" in message

def test_add_book_invalid_author_too_long():
    """Test adding a book with an author that's too long."""
    success, message = add_book_to_catalog("Guinness World Records: Longest Personal Name", "Adolph Blaine Charles David Earl Frederick Gerald Hubert Irvin John Kenneth Lloyd Martin Nero Oliver Paul Quincy Randolph Sherman Thomas Uncas Victor William Xerxes Yancy Zeus Wolfstern", "6665855901019", 7)
    
    assert success == False
    assert "Author must be less" in message

def test_add_book_invalid_isbn_not_digits():
    """Test adding a book with ISBN with other characters that aren't digits."""
    success, message = add_book_to_catalog("The Study of Digitology", "Ownley Careicters", "ThisWillFail!", 3)
    
    assert success == False
    assert "only digits" in message


