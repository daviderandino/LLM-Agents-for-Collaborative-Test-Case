import pytest
from data.input_code.04_library import *

# ------------------------------------------------------------------
# Book tests
# ------------------------------------------------------------------
def test_book_init():
    book = Book("Test Book", "Test Author", "1234567890")
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.isbn == "1234567890"
    assert book.is_available is True

def test_book_str():
    book = Book("Test Book", "Test Author", "1234567890")
    expected = "[Available] Test Book by Test Author (ISBN: 1234567890)"
    assert str(book) == expected

# ------------------------------------------------------------------
# LibraryManager tests
# ------------------------------------------------------------------
def test_library_manager_init():
    lib = LibraryManager()
    assert isinstance(lib.inventory, dict)
    assert lib.inventory == {}

# ------------------------------------------------------------------
# add_book tests
# ------------------------------------------------------------------
@pytest.mark.parametrize(
    "title, author, isbn, expected_output",
    [
        ("Test Book", "Test Author", "1234567890",
         "Success: Added 'Test Book' to the library."),
        ("Test Book", "Test Author", "12",
         "[!] Error: ISBN '12' is too short."),
    ],
)
def test_add_book_success_and_short_isbn(capsys, title, author, isbn, expected_output):
    lib = LibraryManager()
    lib.add_book(title, author, isbn)
    out, _ = capsys.readouterr()
    assert expected_output in out
    if len(isbn) >= 3:
        assert isbn in lib.inventory
    else:
        assert isbn not in lib.inventory

def test_add_book_duplicate_isbn(capsys):
    lib = LibraryManager()
    # First addition should succeed
    lib.add_book("Test Book", "Test Author", "1234567890")
    out1, _ = capsys.readouterr()
    assert "Success: Added 'Test Book' to the library." in out1
    # Duplicate addition should fail
    lib.add_book("Test Book", "Test Author", "1234567890")
    out2, _ = capsys.readouterr()
    assert "[!] Error: A book with ISBN 1234567890 already exists." in out2
    # Inventory should still contain only one book
    assert len(lib.inventory) == 1

# ------------------------------------------------------------------
# borrow_book tests
# ------------------------------------------------------------------
@pytest.mark.parametrize(
    "isbn, expected_output",
    [
        ("1234567890", "Success: You have borrowed 'Test Book'."),
        ("9876543210", "[!] Error: Book with ISBN 9876543210 not found."),
    ],
)
def test_borrow_book(capsys, isbn, expected_output):
    lib = LibraryManager()
    # Add a book only for the first case
    if isbn == "1234567890":
        lib.add_book("Test Book", "Test Author", isbn)
    lib.borrow_book(isbn)
    out, _ = capsys.readouterr()
    assert expected_output in out
    if isbn == "1234567890":
        assert not lib.inventory[isbn].is_available

def test_borrow_book_already_borrowed(capsys):
    lib = LibraryManager()
    lib.add_book("Test Book", "Test Author", "1234567890")
    lib.borrow_book("1234567890")  # First borrow
    out1, _ = capsys.readouterr()
    assert "Success: You have borrowed 'Test Book'." in out1
    lib.borrow_book("1234567890")  # Second borrow attempt
    out2, _ = capsys.readouterr()
    assert "[!] Unavailable: 'Test Book' is currently borrowed by someone else." in out2

# ------------------------------------------------------------------
# return_book tests
# ------------------------------------------------------------------
@pytest.mark.parametrize(
    "isbn, expected_output",
    [
        ("1234567890", "Success: 'Test Book' has been returned."),
        ("9876543210", "[!] Error: We do not own a book with ISBN 9876543210."),
    ],
)
def test_return_book(capsys, isbn, expected_output):
    lib = LibraryManager()
    if isbn == "1234567890":
        lib.add_book("Test Book", "Test Author", isbn)
        lib.borrow_book(isbn)  # Borrow first
    lib.return_book(isbn)
    out, _ = capsys.readouterr()
    assert expected_output in out
    if isbn == "1234567890":
        assert lib.inventory[isbn].is_available

def test_return_book_already_available(capsys):
    lib = LibraryManager()
    lib.add_book("Test Book", "Test Author", "1234567890")
    lib.return_book("1234567890")  # Return without borrowing
    out, _ = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'Test Book', but it was already here." in out

# ------------------------------------------------------------------
# show_inventory tests
# ------------------------------------------------------------------
def test_show_inventory_empty(capsys):
    lib = LibraryManager()
    lib.show_inventory()
    out, _ = capsys.readouterr()
    assert "The library is empty." in out

def test_show_inventory_non_empty(capsys):
    lib = LibraryManager()
    lib.add_book("Test Book", "Test Author", "1234567890")
    lib.show_inventory()
    out, _ = capsys.readouterr()
    assert "[Available] Test Book by Test Author (ISBN: 1234567890)" in out