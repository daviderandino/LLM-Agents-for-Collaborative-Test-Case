import pytest
from data.input_code.d07_library import *

# Fixtures
@pytest.fixture
def empty_manager():
    """Provides a fresh LibraryManager with no books."""
    return LibraryManager()

@pytest.fixture
def manager_with_one_book():
    """LibraryManager pre-populated with a single book (available)."""
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")
    return lm

# ------------------- Book Tests ------------------- #

def test_book_init():
    b = Book("Test Book", "Test Author", "1234567890")
    assert b.title == "Test Book"
    assert b.author == "Test Author"
    assert b.isbn == "1234567890"
    assert b.is_available is True

def test_book_str():
    b = Book("Test Book", "Test Author", "1234567890")
    expected = "[Available] Test Book by Test Author (ISBN: 1234567890)"
    assert str(b) == expected

# ------------------- LibraryManager Init ------------------- #

def test_library_manager_init(empty_manager):
    assert isinstance(empty_manager.inventory, dict)
    assert not empty_manager.inventory  # should be empty

# ------------------- add_book Tests ------------------- #

@pytest.mark.parametrize(
    "title, author, isbn, expected_msg, should_add",
    [
        ("Test Book", "Test Author", "1234567890",
         "Success: Added 'Test Book' to the library.", True),
        ("Short ISBN", "Author", "12",
         "[!] Error: ISBN '12' is too short.", False),
    ]
)
def test_add_book_various(empty_manager, title, author, isbn, expected_msg, should_add, capsys):
    empty_manager.add_book(title, author, isbn)
    captured = capsys.readouterr().out.strip()
    assert expected_msg in captured
    if should_add:
        assert isbn in empty_manager.inventory
        book = empty_manager.inventory[isbn]
        assert isinstance(book, Book)
        assert book.title == title
        assert book.author == author
    else:
        assert isbn not in empty_manager.inventory

def test_add_book_duplicate(manager_with_one_book, capsys):
    # Attempt to add a book with the same ISBN as the existing one
    manager_with_one_book.add_book("Another Title", "Another Author", "1234567890")
    captured = capsys.readouterr().out.strip()
    assert "[!] Error: A book with ISBN 1234567890 already exists." in captured
    # Inventory should still contain only the original book
    assert len(manager_with_one_book.inventory) == 1
    original = manager_with_one_book.inventory["1234567890"]
    assert original.title == "Test Book"
    assert original.author == "Test Author"

# ------------------- borrow_book Tests ------------------- #

def test_borrow_book_success(manager_with_one_book, capsys):
    manager_with_one_book.borrow_book("1234567890")
    captured = capsys.readouterr().out.strip()
    assert "Success: You have borrowed 'Test Book'." in captured
    assert manager_with_one_book.inventory["1234567890"].is_available is False

def test_borrow_book_not_found(empty_manager, capsys):
    empty_manager.borrow_book("9876543210")
    captured = capsys.readouterr().out.strip()
    assert "[!] Error: Book with ISBN 9876543210 not found." in captured

def test_borrow_book_unavailable(manager_with_one_book, capsys):
    # Borrow once to make it unavailable
    manager_with_one_book.borrow_book("1234567890")
    capsys.readouterr()  # clear previous output
    # Attempt to borrow again
    manager_with_one_book.borrow_book("1234567890")
    captured = capsys.readouterr().out.strip()
    assert "[!] Unavailable: 'Test Book' is currently borrowed by someone else." in captured
    # Status should remain False
    assert manager_with_one_book.inventory["1234567890"].is_available is False

# ------------------- return_book Tests ------------------- #

def test_return_book_success(manager_with_one_book, capsys):
    # Borrow first so it can be returned
    manager_with_one_book.borrow_book("1234567890")
    capsys.readouterr()
    manager_with_one_book.return_book("1234567890")
    captured = capsys.readouterr().out.strip()
    assert "Success: 'Test Book' has been returned." in captured
    assert manager_with_one_book.inventory["1234567890"].is_available is True

def test_return_book_not_found(empty_manager, capsys):
    empty_manager.return_book("9876543210")
    captured = capsys.readouterr().out.strip()
    assert "[!] Error: We do not own a book with ISBN 9876543210." in captured

def test_return_book_already_available(manager_with_one_book, capsys):
    # Book is initially available; attempt to return without borrowing
    manager_with_one_book.return_book("1234567890")
    captured = capsys.readouterr().out.strip()
    assert "[!] Strange: You are trying to return 'Test Book', but it was already here." in captured
    assert manager_with_one_book.inventory["1234567890"].is_available is True

# ------------------- show_inventory Tests ------------------- #

def test_show_inventory_empty(empty_manager, capsys):
    empty_manager.show_inventory()
    captured = capsys.readouterr().out
    assert "The library is empty." in captured

def test_show_inventory_not_empty(manager_with_one_book, capsys):
    manager_with_one_book.show_inventory()
    captured = capsys.readouterr().out
    # Header and footer are present
    assert "--- Current Library Inventory ---" in captured
    # Book line should appear with correct status
    expected_line = "[Available] Test Book by Test Author (ISBN: 1234567890)"
    assert expected_line in captured
    assert "---------------------------------" in captured