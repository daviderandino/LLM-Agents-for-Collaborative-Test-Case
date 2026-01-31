import pytest
from data.input_code.d04_library import *

@pytest.fixture
def manager():
    """Provides a fresh LibraryManager for each test."""
    return LibraryManager()

def test_add_book_success(manager, capsys):
    manager.add_book("Book Title", "Author Name", "1234567890")
    captured = capsys.readouterr()
    assert "Success: Added 'Book Title' to the library." in captured.out
    assert "1234567890" in manager.inventory
    book = manager.inventory["1234567890"]
    assert isinstance(book, Book)
    assert book.title == "Book Title"
    assert book.author == "Author Name"
    assert book.is_available is True

def test_add_book_isbn_too_short(manager, capsys):
    manager.add_book("Book Title", "Author Name", "12")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out
    assert "12" not in manager.inventory

def test_add_book_duplicate_isbn(manager, capsys):
    manager.add_book("First Book", "Author A", "1234567890")
    manager.add_book("Second Book", "Author B", "1234567890")
    captured = capsys.readouterr()
    # The second call should trigger duplicate error
    assert "[!] Error: A book with ISBN 1234567890 already exists." in captured.out
    # Inventory should contain only the first book
    assert len(manager.inventory) == 1
    assert manager.inventory["1234567890"].title == "First Book"

@pytest.fixture
def manager_with_book():
    """LibraryManager with a single available book."""
    lm = LibraryManager()
    lm.add_book("Book Title", "Author Name", "1234567890")
    return lm

@pytest.mark.parametrize(
    "isbn,expected_output,expected_available",
    [
        ("1234567890", "Success: You have borrowed 'Book Title'.", False),  # successful borrow
    ],
)
def test_borrow_book_success(manager_with_book, isbn, expected_output, expected_available, capsys):
    manager_with_book.borrow_book(isbn)
    captured = capsys.readouterr()
    assert expected_output in captured.out
    assert manager_with_book.inventory[isbn].is_available == expected_available

def test_borrow_book_not_found(manager, capsys):
    manager.borrow_book("9876543210")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN 9876543210 not found." in captured.out

def test_borrow_book_not_available(manager_with_book, capsys):
    # Borrow once to make it unavailable
    manager_with_book.borrow_book("1234567890")
    capsys.readouterr()  # clear previous output
    # Attempt second borrow
    manager_with_book.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Unavailable: 'Book Title' is currently borrowed by someone else." in captured.out

@pytest.mark.parametrize(
    "setup_action, isbn, expected_msg, final_status",
    [
        ("borrowed", "1234567890", "Success: 'Book Title' has been returned.", True),   # return after borrow
        ("none", "9876543210", "[!] Error: We do not own a book with ISBN 9876543210.", None),  # not owned
        ("available", "1234567890", "[!] Strange: You are trying to return 'Book Title', but it was already here.", True),  # already available
    ],
)
def test_return_book_cases(manager, setup_action, isbn, expected_msg, final_status, capsys):
    # Prepare state based on setup_action
    if setup_action != "none":
        manager.add_book("Book Title", "Author Name", "1234567890")
    if setup_action == "borrowed":
        manager.borrow_book("1234567890")
        capsys.readouterr()  # clear output
    elif setup_action == "available":
        # book already added and is available; nothing else needed
        pass

    manager.return_book(isbn)
    captured = capsys.readouterr()
    assert expected_msg in captured.out
    if final_status is not None:
        assert manager.inventory[isbn].is_available == final_status

def test_show_inventory(manager_with_book, capsys):
    manager_with_book.show_inventory()
    captured = capsys.readouterr()
    output = captured.out
    assert "--- Current Library Inventory ---" in output
    assert "[Available] Book Title by Author Name (ISBN: 1234567890)" in output
    assert "---------------------------------" in output