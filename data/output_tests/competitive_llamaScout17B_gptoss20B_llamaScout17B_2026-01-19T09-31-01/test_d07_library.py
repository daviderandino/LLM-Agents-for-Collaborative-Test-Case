import pytest
from data.input_code.d07_library import *

@pytest.fixture
def lib():
    """Return a fresh LibraryManager instance for each test."""
    return LibraryManager()

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

def test_add_book_success(lib, capsys):
    lib.add_book("Test Book", "Test Author", "1234567890")
    assert "1234567890" in lib.inventory
    captured = capsys.readouterr()
    assert "Success: Added 'Test Book' to the library." in captured.out

def test_add_book_isbn_too_short(lib, capsys):
    lib.add_book("Short ISBN", "Author", "12")
    assert "12" not in lib.inventory
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out

def test_add_book_duplicate(lib, capsys):
    lib.add_book("Test Book", "Test Author", "1234567890")
    lib.add_book("Test Book", "Test Author", "1234567890")
    assert len(lib.inventory) == 1
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 1234567890 already exists." in captured.out

def test_borrow_book_success(lib, capsys):
    lib.add_book("Test Book", "Test Author", "1234567890")
    lib.borrow_book("1234567890")
    assert lib.inventory["1234567890"].is_available is False
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'Test Book'." in captured.out

def test_borrow_book_not_found(lib, capsys):
    lib.borrow_book("9876543210")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN 9876543210 not found." in captured.out

def test_borrow_book_unavailable(lib, capsys):
    lib.add_book("Test Book", "Test Author", "1234567890")
    lib.borrow_book("1234567890")
    lib.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Unavailable: 'Test Book' is currently borrowed by someone else." in captured.out
    assert lib.inventory["1234567890"].is_available is False

def test_return_book_success(lib, capsys):
    lib.add_book("Test Book", "Test Author", "1234567890")
    lib.borrow_book("1234567890")
    lib.return_book("1234567890")
    assert lib.inventory["1234567890"].is_available is True
    captured = capsys.readouterr()
    assert "Success: 'Test Book' has been returned." in captured.out

def test_return_book_not_found(lib, capsys):
    lib.return_book("9876543210")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN 9876543210." in captured.out

def test_return_book_already_available(lib, capsys):
    lib.add_book("Test Book", "Test Author", "1234567890")
    lib.return_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'Test Book', but it was already here." in captured.out
    assert lib.inventory["1234567890"].is_available is True

def test_show_inventory_empty(lib, capsys):
    lib.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_show_inventory_not_empty(lib, capsys):
    lib.add_book("Test Book", "Test Author", "1234567890")
    lib.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Test Book by Test Author (ISBN: 1234567890)" in captured.out