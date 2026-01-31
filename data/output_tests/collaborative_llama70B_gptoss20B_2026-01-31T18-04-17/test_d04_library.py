import pytest
from data.input_code.d04_library import *

# --------------------------------------------------------------------------- #
# Book tests
# --------------------------------------------------------------------------- #

def test_book_init():
    """T1_BOOK_INIT – Book initialization."""
    book = Book("Test Book", "Test Author", "1234567890")
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.isbn == "1234567890"
    assert book.is_available is True

def test_book_str():
    """T2_BOOK_STR – Book string representation."""
    book = Book("Test Book", "Test Author", "1234567890")
    expected = "[Available] Test Book by Test Author (ISBN: 1234567890)"
    assert str(book) == expected

# --------------------------------------------------------------------------- #
# LibraryManager tests
# --------------------------------------------------------------------------- #

def test_library_init():
    """T3_LIB_INIT – Library initialization."""
    lib = LibraryManager()
    assert isinstance(lib.inventory, dict)
    assert lib.inventory == {}

# --------------------------------------------------------------------------- #
# add_book tests
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "title,author,isbn,expected_output",
    [
        ("Test Book", "Test Author", "1234567890",
         "Success: Added 'Test Book' to the library.\n"),
    ],
)
def test_add_book_success(capsys, title, author, isbn, expected_output):
    lib = LibraryManager()
    lib.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out == expected_output
    # Ensure book is stored
    assert isbn in lib.inventory
    assert lib.inventory[isbn].title == title

@pytest.mark.parametrize(
    "title,author,isbn,expected_output",
    [
        ("Test Book", "Test Author", "12",
         "[!] Error: ISBN '12' is too short.\n"),
    ],
)
def test_add_book_short_isbn(capsys, title, author, isbn, expected_output):
    lib = LibraryManager()
    lib.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out == expected_output
    assert isbn not in lib.inventory

@pytest.mark.parametrize(
    "title,author,isbn,expected_output",
    [
        ("Test Book", "Test Author", "1234567890",
         "[!] Error: A book with ISBN 1234567890 already exists.\n"),
    ],
)
def test_add_book_duplicate(capsys, title, author, isbn, expected_output):
    lib = LibraryManager()
    # First addition
    lib.add_book(title, author, isbn)
    # Second addition triggers duplicate
    lib.add_book(title, author, isbn)
    captured = capsys.readouterr()
    # The second call's output is the last line printed
    assert captured.out.splitlines()[-1] + "\n" == expected_output

# --------------------------------------------------------------------------- #
# borrow_book tests
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "isbn,expected_output",
    [
        ("1234567890", "Success: Added 'Test Book' to the library.\nSuccess: You have borrowed 'Test Book'.\n"),
    ],
)
def test_borrow_book_success(capsys, isbn, expected_output):
    lib = LibraryManager()
    lib.add_book("Test Book", "Test Author", isbn)
    lib.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out == expected_output
    assert lib.inventory[isbn].is_available is False

@pytest.mark.parametrize(
    "isbn,expected_output",
    [
        ("9876543210", "[!] Error: Book with ISBN 9876543210 not found.\n"),
    ],
)
def test_borrow_book_not_found(capsys, isbn, expected_output):
    lib = LibraryManager()
    lib.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out == expected_output

@pytest.mark.parametrize(
    "isbn,expected_output",
    [
        ("1234567890", "[!] Unavailable: 'Test Book' is currently borrowed by someone else.\n"),
    ],
)
def test_borrow_book_unavailable(capsys, isbn, expected_output):
    lib = LibraryManager()
    lib.add_book("Test Book", "Test Author", isbn)
    lib.borrow_book(isbn)  # first borrow
    lib.borrow_book(isbn)  # second borrow triggers unavailable
    captured = capsys.readouterr()
    # The second borrow's output is the last line printed
    assert captured.out.splitlines()[-1] + "\n" == expected_output

# --------------------------------------------------------------------------- #
# return_book tests
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "isbn,expected_output",
    [
        ("1234567890", "Success: Added 'Test Book' to the library.\nSuccess: You have borrowed 'Test Book'.\nSuccess: 'Test Book' has been returned.\n"),
    ],
)
def test_return_book_success(capsys, isbn, expected_output):
    lib = LibraryManager()
    lib.add_book("Test Book", "Test Author", isbn)
    lib.borrow_book(isbn)
    lib.return_book(isbn)
    captured = capsys.readouterr()
    assert captured.out == expected_output
    assert lib.inventory[isbn].is_available is True

@pytest.mark.parametrize(
    "isbn,expected_output",
    [
        ("9876543210", "[!] Error: We do not own a book with ISBN 9876543210.\n"),
    ],
)
def test_return_book_not_found(capsys, isbn, expected_output):
    lib = LibraryManager()
    lib.return_book(isbn)
    captured = capsys.readouterr()
    assert captured.out == expected_output

@pytest.mark.parametrize(
    "isbn,expected_output",
    [
        ("1234567890", "Success: Added 'Test Book' to the library.\n[!] Strange: You are trying to return 'Test Book', but it was already here.\n"),
    ],
)
def test_return_book_already_returned(capsys, isbn, expected_output):
    lib = LibraryManager()
    lib.add_book("Test Book", "Test Author", isbn)
    lib.return_book(isbn)  # first return (book was available)
    captured = capsys.readouterr()
    assert captured.out == expected_output

# --------------------------------------------------------------------------- #
# show_inventory test
# --------------------------------------------------------------------------- #

def test_show_inventory(capsys):
    """T13_SHOW_INVENTORY – Show library inventory."""
    lib = LibraryManager()
    lib.show_inventory()
    captured = capsys.readouterr()
    # Inventory is empty, so check for the empty message
    assert "The library is empty." in captured.out

    # Add a book and check representation
    lib.add_book("Test Book", "Test Author", "1234567890")
    lib.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Test Book by Test Author (ISBN: 1234567890)" in captured.out