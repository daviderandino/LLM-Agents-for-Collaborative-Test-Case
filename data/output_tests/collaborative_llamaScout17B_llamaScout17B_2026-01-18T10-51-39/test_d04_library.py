import pytest
from data.input_code.d04_library import *

# Fixtures
@pytest.fixture
def library_manager():
    return LibraryManager()

# Helper functions
def capture_printed_output(func):
    import io
    import sys
    captured_output = io.StringIO()                  # Create StringIO object
    sys.stdout = captured_output                     # Redirect stdout
    func()
    sys.stdout = sys.__stdout__                     # Reset stdout
    return captured_output.getvalue().strip()         # Return captured output

# Test cases
def test_add_book_success(library_manager):
    result = capture_printed_output(lambda: library_manager.add_book("Book Title", "Author Name", "1234567890"))
    assert result == "Success: Added 'Book Title' to the library."

def test_add_book_isbn_too_short(library_manager):
    result = capture_printed_output(lambda: library_manager.add_book("Book Title", "Author Name", "12"))
    assert result == "[!] Error: ISBN '12' is too short."

def test_add_book_duplicate_isbn(library_manager):
    library_manager.add_book("Book Title", "Author Name", "1234567890")
    result = capture_printed_output(lambda: library_manager.add_book("Book Title", "Author Name", "1234567890"))
    assert result == "[!] Error: A book with ISBN 1234567890 already exists."

@pytest.mark.parametrize("isbn, message", [
    ("1234567891", "[!] Error: Book with ISBN 1234567891 not found."),
    ("1234567890", "Success: You have borrowed 'Book Title'.")
])
def test_borrow_book(library_manager, isbn, message):
    if isbn == "1234567890":
        library_manager.add_book("Book Title", "Author Name", isbn)
    result = capture_printed_output(lambda: library_manager.borrow_book(isbn))
    assert result == message

def test_borrow_book_already_borrowed(library_manager):
    library_manager.add_book("Book Title", "Author Name", "1234567890")
    library_manager.borrow_book("1234567890")
    result = capture_printed_output(lambda: library_manager.borrow_book("1234567890"))
    assert result == "[!] Unavailable: 'Book Title' is currently borrowed by someone else."

@pytest.mark.parametrize("isbn, message", [
    ("1234567891", "[!] Error: We do not own a book with ISBN 1234567891."),
    ("1234567890", "Success: 'Book Title' has been returned.")
])
def test_return_book(library_manager, isbn, message):
    if isbn == "1234567890":
        library_manager.add_book("Book Title", "Author Name", isbn)
        library_manager.borrow_book(isbn)
    result = capture_printed_output(lambda: library_manager.return_book(isbn))
    assert result == message

def test_return_book_already_available(library_manager):
    library_manager.add_book("Book Title", "Author Name", "1234567890")
    result = capture_printed_output(lambda: library_manager.return_book("1234567890"))
    assert result == "[!] Strange: You are trying to return 'Book Title', but it was already here."

def test_show_inventory_empty(library_manager):
    result = capture_printed_output(library_manager.show_inventory)
    assert result == "--- Current Library Inventory ---\nThe library is empty.\n---------------------------------"

def test_show_inventory_non_empty(library_manager):
    library_manager.add_book("Book Title", "Author Name", "1234567890")
    result = capture_printed_output(library_manager.show_inventory)
    assert "Book Title by Author Name (ISBN: 1234567890)" in result