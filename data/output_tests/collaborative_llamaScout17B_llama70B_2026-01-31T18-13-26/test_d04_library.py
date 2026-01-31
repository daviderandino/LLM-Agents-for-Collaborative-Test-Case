import pytest
from data.input_code.d04_library import *

@pytest.fixture
def library_manager():
    return LibraryManager()

def test_add_book_success(library_manager, capsys):
    library_manager.add_book("Test Book", "Test Author", "123456789")
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Test Book' to the library.\n"

def test_add_book_error_isbn_too_short(library_manager, capsys):
    library_manager.add_book("Test Book", "Test Author", "12")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: ISBN '12' is too short.\n"

def test_add_book_error_duplicate_isbn(library_manager, capsys):
    library_manager.add_book("Test Book", "Test Author", "123456789")
    library_manager.add_book("Test Book", "Test Author", "123456789")
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Test Book' to the library.\n[!] Error: A book with ISBN 123456789 already exists.\n"

def test_borrow_book_success(library_manager, capsys):
    library_manager.add_book("Test Book", "Test Author", "123456789")
    library_manager.borrow_book("123456789")
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Test Book' to the library.\nSuccess: You have borrowed 'Test Book'.\n"

def test_borrow_book_error_book_not_found(library_manager, capsys):
    library_manager.borrow_book("987654321")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: Book with ISBN 987654321 not found.\n"

def test_borrow_book_error_book_already_borrowed(library_manager, capsys):
    library_manager.add_book("Test Book", "Test Author", "123456789")
    library_manager.borrow_book("123456789")
    library_manager.borrow_book("123456789")
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Test Book' to the library.\nSuccess: You have borrowed 'Test Book'.\n[!] Unavailable: 'Test Book' is currently borrowed by someone else.\n"

def test_return_book_success(library_manager, capsys):
    library_manager.add_book("Test Book", "Test Author", "123456789")
    library_manager.borrow_book("123456789")
    library_manager.return_book("123456789")
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Test Book' to the library.\nSuccess: You have borrowed 'Test Book'.\nSuccess: 'Test Book' has been returned.\n"

def test_return_book_error_book_not_found(library_manager, capsys):
    library_manager.return_book("987654321")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: We do not own a book with ISBN 987654321.\n"

def test_return_book_error_book_already_available(library_manager, capsys):
    library_manager.add_book("Test Book", "Test Author", "123456789")
    library_manager.return_book("123456789")
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Test Book' to the library.\n[!] Strange: You are trying to return 'Test Book', but it was already here.\n"


