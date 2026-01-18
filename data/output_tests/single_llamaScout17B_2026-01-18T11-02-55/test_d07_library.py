import pytest
from data.input_code.d07_library import Book, LibraryManager

def test_book_init():
    book = Book("Test Title", "Test Author", "1234567890")
    assert book.title == "Test Title"
    assert book.author == "Test Author"
    assert book.isbn == "1234567890"
    assert book.is_available

def test_book_str_available():
    book = Book("Test Title", "Test Author", "1234567890")
    assert str(book) == "[Available] Test Title by Test Author (ISBN: 1234567890)"

def test_book_str_borrowed():
    book = Book("Test Title", "Test Author", "1234567890")
    book.is_available = False
    assert str(book) == "[Borrowed] Test Title by Test Author (ISBN: 1234567890)"

def test_library_manager_init():
    manager = LibraryManager()
    assert manager.inventory == {}

def test_library_manager_add_book_success():
    manager = LibraryManager()
    manager.add_book("Test Title", "Test Author", "1234567890")
    assert len(manager.inventory) == 1

def test_library_manager_add_book_isbn_too_short(capsys):
    manager = LibraryManager()
    manager.add_book("Test Title", "Test Author", "12")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: ISBN '12' is too short.\n"

def test_library_manager_add_book_duplicate(capsys):
    manager = LibraryManager()
    manager.add_book("Test Title", "Test Author", "1234567890")
    manager.add_book("Test Title 2", "Test Author 2", "1234567890")
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Test Title' to the library.\n[!] Error: A book with ISBN 1234567890 already exists.\n"

def test_library_manager_borrow_book_success(capsys):
    manager = LibraryManager()
    manager.add_book("Test Title", "Test Author", "1234567890")
    manager.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out.endswith("Success: You have borrowed 'Test Title'.\n")

def test_library_manager_borrow_book_not_found(capsys):
    manager = LibraryManager()
    manager.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: Book with ISBN 1234567890 not found.\n"

def test_library_manager_borrow_book_unavailable(capsys):
    manager = LibraryManager()
    manager.add_book("Test Title", "Test Author", "1234567890")
    manager.borrow_book("1234567890")
    manager.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out.endswith("[!] Unavailable: 'Test Title' is currently borrowed by someone else.\n")

def test_library_manager_return_book_success(capsys):
    manager = LibraryManager()
    manager.add_book("Test Title", "Test Author", "1234567890")
    manager.borrow_book("1234567890")
    manager.return_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out.endswith("Success: 'Test Title' has been returned.\n")

def test_library_manager_return_book_not_found(capsys):
    manager = LibraryManager()
    manager.return_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: We do not own a book with ISBN 1234567890.\n"


def test_library_manager_show_inventory_empty():
    manager = LibraryManager()
    manager.show_inventory()
    # No direct way to test print output, but we can verify it doesn't throw an error

def test_library_manager_show_inventory_not_empty(capsys):
    manager = LibraryManager()
    manager.add_book("Test Title", "Test Author", "1234567890")
    manager.show_inventory()
    captured = capsys.readouterr()
    assert "Current Library Inventory" in captured.out
    assert "Test Title" in captured.out

def test_book_edge_cases():
    book = Book("", "", "")
    assert book.title == ""
    assert book.author == ""
    assert book.isbn == ""

