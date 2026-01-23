import pytest
from data.input_code.d07_library import Book, LibraryManager

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
    manager = LibraryManager()
    assert manager.inventory == {}

def test_add_book_valid():
    manager = LibraryManager()
    manager.add_book("Title", "Author", "1234567890")
    assert "1234567890" in manager.inventory

def test_add_book_invalid_isbn_length():
    manager = LibraryManager()
    manager.add_book("Title", "Author", "12")
    assert "12" not in manager.inventory

def test_add_book_duplicate_isbn():
    manager = LibraryManager()
    manager.add_book("Title1", "Author1", "1234567890")
    manager.add_book("Title2", "Author2", "1234567890")
    assert len(manager.inventory) == 1

def test_borrow_book_existing_and_available():
    manager = LibraryManager()
    manager.add_book("Title", "Author", "1234567890")
    manager.borrow_book("1234567890")
    assert manager.inventory["1234567890"].is_available == False

def test_borrow_book_non_existing():
    manager = LibraryManager()
    manager.borrow_book("1234567890")
    assert manager.inventory == {}

def test_borrow_book_already_borrowed():
    manager = LibraryManager()
    manager.add_book("Title", "Author", "1234567890")
    manager.borrow_book("1234567890")
    manager.borrow_book("1234567890")
    assert manager.inventory["1234567890"].is_available == False

def test_return_book_existing_and_borrowed():
    manager = LibraryManager()
    manager.add_book("Title", "Author", "1234567890")
    manager.borrow_book("1234567890")
    manager.return_book("1234567890")
    assert manager.inventory["1234567890"].is_available == True

def test_return_book_non_existing():
    manager = LibraryManager()
    manager.return_book("1234567890")
    assert manager.inventory == {}

def test_return_book_not_borrowed():
    manager = LibraryManager()
    manager.add_book("Title", "Author", "1234567890")
    manager.return_book("1234567890")
    assert manager.inventory["1234567890"].is_available == True

def test_show_inventory_empty():
    manager = LibraryManager()
    manager.show_inventory()
    assert manager.inventory == {}

def test_show_inventory_non_empty():
    manager = LibraryManager()
    manager.add_book("Title1", "Author1", "1234567890")
    manager.add_book("Title2", "Author2", "0987654321")
    assert len(manager.inventory) == 2