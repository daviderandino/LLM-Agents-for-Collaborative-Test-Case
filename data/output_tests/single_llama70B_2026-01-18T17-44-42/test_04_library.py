import pytest
from data.input_code.04_library import Book, LibraryManager

def test_book_init():
    book = Book("Test Book", "Test Author", "1234567890")
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.isbn == "1234567890"
    assert book.is_available

def test_book_str():
    book = Book("Test Book", "Test Author", "1234567890")
    assert str(book) == "[Available] Test Book by Test Author (ISBN: 1234567890)"

def test_library_manager_init():
    library = LibraryManager()
    assert not library.inventory

def test_add_book_success(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    assert "1234567890" in library.inventory
    captured = capsys.readouterr()
    assert "Success: Added 'Test Book' to the library." in captured.out

def test_add_book_duplicate(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.add_book("Test Book 2", "Test Author 2", "1234567890")
    captured = capsys.readouterr()
    assert "Error: A book with ISBN 1234567890 already exists." in captured.out

def test_add_book_invalid_isbn(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "12")
    captured = capsys.readouterr()
    assert "Error: ISBN '12' is too short." in captured.out

def test_borrow_book_success(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'Test Book'." in captured.out
    assert not library.inventory["1234567890"].is_available

def test_borrow_book_unavailable(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.borrow_book("1234567890")
    library.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert "Unavailable: 'Test Book' is currently borrowed by someone else." in captured.out

def test_borrow_book_not_found(capsys):
    library = LibraryManager()
    library.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert "Error: Book with ISBN 1234567890 not found." in captured.out

def test_return_book_success(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.borrow_book("1234567890")
    library.return_book("1234567890")
    captured = capsys.readouterr()
    assert "Success: 'Test Book' has been returned." in captured.out
    assert library.inventory["1234567890"].is_available

def test_return_book_not_borrowed(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.return_book("1234567890")
    captured = capsys.readouterr()
    assert "Strange: You are trying to return 'Test Book', but it was already here." in captured.out

def test_return_book_not_found(capsys):
    library = LibraryManager()
    library.return_book("1234567890")
    captured = capsys.readouterr()
    assert "Error: We do not own a book with ISBN 1234567890." in captured.out

def test_show_inventory_empty(capsys):
    library = LibraryManager()
    library.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_show_inventory_not_empty(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Test Book by Test Author (ISBN: 1234567890)" in captured.out