import pytest
from data.input_code.d07_library import *

# ---------- Book tests ----------
def test_book_init():
    b = Book(title="Test Book", author="Test Author", isbn="1234567890")
    assert b.title == "Test Book"
    assert b.author == "Test Author"
    assert b.isbn == "1234567890"
    assert b.is_available is True

def test_book_str():
    b = Book(title="Test Book", author="Test Author", isbn="1234567890")
    expected = "[Available] Test Book by Test Author (ISBN: 1234567890)"
    assert str(b) == expected

# ---------- LibraryManager initialization ----------
def test_library_manager_init():
    lm = LibraryManager()
    assert isinstance(lm.inventory, dict)
    assert not lm.inventory  # should be empty

# ---------- add_book ----------
@pytest.mark.parametrize(
    "title, author, isbn, expected_output",
    [
        (
            "Test Book",
            "Test Author",
            "1234567890",
            "Success: Added 'Test Book' to the library.\n",
        ),
        (
            "Test Book",
            "Test Author",
            "12",
            "[!] Error: ISBN '12' is too short.\n",
        ),
    ],
)
def test_add_book_various(title, author, isbn, expected_output, capsys):
    lm = LibraryManager()
    lm.add_book(title, author, isbn)
    captured = capsys.readouterr()
    # add_book prints a trailing newline via print, so we compare the line content
    assert captured.out.strip() == expected_output.strip()

def test_add_book_duplicate_isbn(capsys):
    lm = LibraryManager()
    # first addition (valid)
    lm.add_book("Test Book", "Test Author", "1234567890")
    capsys.readouterr()  # clear first output
    # duplicate addition
    lm.add_book("Another Title", "Another Author", "1234567890")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: A book with ISBN 1234567890 already exists."

# ---------- borrow_book ----------
def test_borrow_book_success(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")
    capsys.readouterr()  # clear add_book output
    lm.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: You have borrowed 'Test Book'."

def test_borrow_book_not_found(capsys):
    lm = LibraryManager()
    lm.borrow_book("9876543210")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: Book with ISBN 9876543210 not found."

def test_borrow_book_unavailable(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")
    capsys.readouterr()
    # first borrow succeeds
    lm.borrow_book("1234567890")
    capsys.readouterr()
    # second borrow should report unavailable
    lm.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Unavailable: 'Test Book' is currently borrowed by someone else."

# ---------- return_book ----------
def test_return_book_success(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")
    capsys.readouterr()
    lm.borrow_book("1234567890")
    capsys.readouterr()
    lm.return_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: 'Test Book' has been returned."

def test_return_book_not_found(capsys):
    lm = LibraryManager()
    lm.return_book("9876543210")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: We do not own a book with ISBN 9876543210."

def test_return_book_already_returned(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")
    capsys.readouterr()
    # attempt to return without borrowing first
    lm.return_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Strange: You are trying to return 'Test Book', but it was already here."

# ---------- show_inventory ----------
def test_show_inventory_empty(capsys):
    lm = LibraryManager()
    lm.show_inventory()
    captured = capsys.readouterr()
    # The method prints a header, the message, and a footer.
    lines = [line.strip() for line in captured.out.strip().splitlines() if line.strip()]
    assert lines == ["--- Current Library Inventory ---", "The library is empty.", "---------------------------------"]

def test_show_inventory_non_empty(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")
    capsys.readouterr()
    lm.show_inventory()
    captured = capsys.readouterr()
    lines = [line.strip() for line in captured.out.strip().splitlines() if line.strip()]
    # Expected order: header, book string, footer
    expected_book_str = "[Available] Test Book by Test Author (ISBN: 1234567890)"
    assert lines == ["--- Current Library Inventory ---", expected_book_str, "---------------------------------"]