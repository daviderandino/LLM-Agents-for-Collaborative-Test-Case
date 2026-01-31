import pytest
from data.input_code.d04_library import *

@pytest.mark.parametrize('title, author, isbn', [
    ("Test Book", "Test Author", "1234567890")
])
def test_book_init(title, author, isbn):
    book = Book(title, author, isbn)
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn
    assert book.is_available

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("Test Book", "Test Author", "1234567890", "[Available] Test Book by Test Author (ISBN: 1234567890)")
])
def test_book_str(title, author, isbn, expected):
    book = Book(title, author, isbn)
    assert str(book) == expected

def test_library_init():
    library = LibraryManager()
    assert library.inventory == {}

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("Test Book", "Test Author", "1234567890", "Success: Added 'Test Book' to the library.")
])
def test_add_book_ok(capsys, title, author, isbn, expected):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert expected in captured.out

def test_add_book_duplicate(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.add_book("Test Book", "Test Author", "1234567890")
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 1234567890 already exists." in captured.out

def test_add_book_invalid_isbn(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "12")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out

@pytest.mark.parametrize('isbn, expected', [
    ("1234567890", "Success: You have borrowed 'Test Book'.")
])
def test_borrow_book_ok(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", isbn)
    library.borrow_book(isbn)
    captured = capsys.readouterr()
    assert expected in captured.out

def test_borrow_book_unavailable(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.borrow_book("1234567890")
    library.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Unavailable: 'Test Book' is currently borrowed by someone else." in captured.out

def test_borrow_book_not_found(capsys):
    library = LibraryManager()
    library.borrow_book("9876543210")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN 9876543210 not found." in captured.out

@pytest.mark.parametrize('isbn, expected', [
    ("1234567890", "Success: 'Test Book' has been returned.")
])
def test_return_book_ok(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", isbn)
    library.borrow_book(isbn)
    library.return_book(isbn)
    captured = capsys.readouterr()
    assert expected in captured.out

def test_return_book_already_returned(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.return_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'Test Book', but it was already here." in captured.out

def test_return_book_not_found(capsys):
    library = LibraryManager()
    library.return_book("9876543210")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN 9876543210." in captured.out

def test_show_inventory_empty(capsys):
    library = LibraryManager()
    library.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_show_inventory_non_empty(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Test Book by Test Author (ISBN: 1234567890)" in captured.out