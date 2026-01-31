import pytest
from data.input_code.d04_library import *

# Fixtures
@pytest.fixture
def library_manager():
    return LibraryManager()

@pytest.fixture
def empty_library_manager():
    return LibraryManager()

# Test cases
def test_add_book_happy_path(library_manager):
    title = "Python 101"
    author = "John Doe"
    isbn = "12345"
    library_manager.add_book(title, author, isbn)
    assert isbn in library_manager.inventory
    assert library_manager.inventory[isbn].title == title
    assert library_manager.inventory[isbn].author == author
    assert library_manager.inventory[isbn].is_available

def test_add_book_isbn_too_short(library_manager, capsys):
    title = "Short ISBN"
    author = "Jane"
    isbn = "12"
    library_manager.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: ISBN '12' is too short.\n"
    assert isbn not in library_manager.inventory

def test_add_book_duplicate_isbn(library_manager, capsys):
    title1 = "Original Book"
    author1 = "Original Author"
    isbn = "12345"
    library_manager.add_book(title1, author1, isbn)
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Original Book' to the library.\n"
    title2 = "Duplicate Book"
    author2 = "Duplicate Author"
    library_manager.add_book(title2, author2, isbn)
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: A book with ISBN 12345 already exists.\n"
    assert len(library_manager.inventory) == 1

def test_borrow_book_non_existent_isbn(library_manager, capsys):
    isbn = "99999"
    library_manager.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: Book with ISBN 99999 not found.\n"

def test_borrow_book_already_borrowed(library_manager, capsys):
    isbn = "12345"
    book = Book("Test Book", "Test Author", isbn)
    library_manager.inventory[isbn] = book
    library_manager.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out == "Success: You have borrowed 'Test Book'.\n"
    library_manager.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out == "[!] Unavailable: 'Test Book' is currently borrowed by someone else.\n"

def test_borrow_book_success(library_manager):
    isbn = "12345"
    book = Book("Test Book", "Test Author", isbn)
    library_manager.inventory[isbn] = book
    library_manager.borrow_book(isbn)
    assert not library_manager.inventory[isbn].is_available

def test_return_book_non_existent_isbn(library_manager, capsys):
    isbn = "88888"
    library_manager.return_book(isbn)
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: We do not own a book with ISBN 88888.\n"

def test_return_book_already_available(library_manager, capsys):
    isbn = "12345"
    book = Book("Test Book", "Test Author", isbn)
    library_manager.inventory[isbn] = book
    library_manager.return_book(isbn)
    captured = capsys.readouterr()
    assert captured.out == "[!] Strange: You are trying to return 'Test Book', but it was already here.\n"

def test_return_book_success(library_manager):
    isbn = "12345"
    book = Book("Test Book", "Test Author", isbn)
    book.is_available = False
    library_manager.inventory[isbn] = book
    library_manager.return_book(isbn)
    assert library_manager.inventory[isbn].is_available

def test_show_inventory_empty(empty_library_manager, capsys):
    empty_library_manager.show_inventory()
    captured = capsys.readouterr()
    assert captured.out == "\n--- Current Library Inventory ---\nThe library is empty.\n---------------------------------\n\n"

def test_show_inventory_non_empty(library_manager, capsys):
    book1 = Book("Book A", "Auth A", "111")
    book2 = Book("Book B", "Auth B", "222")
    book2.is_available = False
    library_manager.inventory["111"] = book1
    library_manager.inventory["222"] = book2
    library_manager.show_inventory()
    captured = capsys.readouterr()
    assert captured.out == "\n--- Current Library Inventory ---\n[Available] Book A by Auth A (ISBN: 111)\n[Borrowed] Book B by Auth B (ISBN: 222)\n---------------------------------\n\n"