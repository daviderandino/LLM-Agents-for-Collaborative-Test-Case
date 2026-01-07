from data.input_code.library import Book, LibraryManager
import pytest
from unittest.mock import patch
from io import StringIO

def test_book_initialization():
    book = Book("Title", "Author", "1234567890")
    assert book.title == "Title"
    assert book.author == "Author"
    assert book.isbn == "1234567890"
    assert book.is_available == True

def test_book_str_representation():
    book = Book("Title", "Author", "1234567890")
    assert str(book) == "[Available] Title by Author (ISBN: 1234567890)"
    book.is_available = False
    assert str(book) == "[Borrowed] Title by Author (ISBN: 1234567890)"

def test_library_manager_initialization():
    library = LibraryManager()
    assert library.inventory == {}

def test_add_book_valid():
    library = LibraryManager()
    with patch('sys.stdout', new=StringIO()) as fake_stdout:
        library.add_book("Title", "Author", "1234567890")
        assert "Success: Added 'Title' to the library." in fake_stdout.getvalue()
        assert "1234567890" in library.inventory

def test_add_book_invalid_isbn():
    library = LibraryManager()
    with patch('sys.stdout', new=StringIO()) as fake_stdout:
        library.add_book("Title", "Author", "12")
        assert "[!] Error: ISBN '12' is too short." in fake_stdout.getvalue()

def test_add_book_duplicate_isbn():
    library = LibraryManager()
    with patch('sys.stdout', new=StringIO()) as fake_stdout:
        library.add_book("Title1", "Author1", "1234567890")
        library.add_book("Title2", "Author2", "1234567890")
        assert "[!] Error: A book with ISBN 1234567890 already exists." in fake_stdout.getvalue()

def test_borrow_book_valid():
    library = LibraryManager()
    library.add_book("Title", "Author", "1234567890")
    with patch('sys.stdout', new=StringIO()) as fake_stdout:
        library.borrow_book("1234567890")
        assert "Success: You have borrowed 'Title'." in fake_stdout.getvalue()
        assert library.inventory["1234567890"].is_available == False

def test_borrow_book_invalid_isbn():
    library = LibraryManager()
    with patch('sys.stdout', new=StringIO()) as fake_stdout:
        library.borrow_book("1234567890")
        assert "[!] Error: Book with ISBN 1234567890 not found." in fake_stdout.getvalue()

def test_borrow_book_already_borrowed():
    library = LibraryManager()
    library.add_book("Title", "Author", "1234567890")
    library.borrow_book("1234567890")
    with patch('sys.stdout', new=StringIO()) as fake_stdout:
        library.borrow_book("1234567890")
        assert "[!] Unavailable: 'Title' is currently borrowed by someone else." in fake_stdout.getvalue()

def test_return_book_valid():
    library = LibraryManager()
    library.add_book("Title", "Author", "1234567890")
    library.borrow_book("1234567890")
    with patch('sys.stdout', new=StringIO()) as fake_stdout:
        library.return_book("1234567890")
        assert "Success: 'Title' has been returned." in fake_stdout.getvalue()
        assert library.inventory["1234567890"].is_available == True

def test_return_book_invalid_isbn():
    library = LibraryManager()
    with patch('sys.stdout', new=StringIO()) as fake_stdout:
        library.return_book("1234567890")
        assert "[!] Error: We do not own a book with ISBN 1234567890." in fake_stdout.getvalue()

def test_return_book_not_borrowed():
    library = LibraryManager()
    library.add_book("Title", "Author", "1234567890")
    with patch('sys.stdout', new=StringIO()) as fake_stdout:
        library.return_book("1234567890")
        assert "[!] Strange: You are trying to return 'Title', but it was already here." in fake_stdout.getvalue()

def test_show_inventory_empty():
    library = LibraryManager()
    with patch('sys.stdout', new=StringIO()) as fake_stdout:
        library.show_inventory()
        assert "The library is empty." in fake_stdout.getvalue()

def test_show_inventory_not_empty():
    library = LibraryManager()
    library.add_book("Title", "Author", "1234567890")
    with patch('sys.stdout', new=StringIO()) as fake_stdout:
        library.show_inventory()
        assert "[Available] Title by Author (ISBN: 1234567890)" in fake_stdout.getvalue()