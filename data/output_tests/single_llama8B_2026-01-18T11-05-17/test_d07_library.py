import pytest
from data.input_code.d07_library import Book, LibraryManager

def test_book_init():
    book = Book("Test Title", "Test Author", "1234567890")
    assert book.title == "Test Title"
    assert book.author == "Test Author"
    assert book.isbn == "1234567890"
    assert book.is_available == True

def test_book_str():
    book = Book("Test Title", "Test Author", "1234567890")
    assert str(book) == "[Available] Test Title by Test Author (ISBN: 1234567890)"

def test_library_manager_init():
    manager = LibraryManager()
    assert manager.inventory == {}

def test_add_book_valid():
    manager = LibraryManager()
    manager.add_book("Test Title", "Test Author", "1234567890")
    assert len(manager.inventory) == 1
    assert manager.inventory["1234567890"].title == "Test Title"

def test_add_book_invalid_isbn():
    manager = LibraryManager()
    manager.add_book("Test Title", "Test Author", "12")
    assert len(manager.inventory) == 0

def test_add_book_duplicate():
    manager = LibraryManager()
    manager.add_book("Test Title", "Test Author", "1234567890")
    manager.add_book("Test Title 2", "Test Author 2", "1234567890")
    assert len(manager.inventory) == 1

def test_borrow_book_valid():
    manager = LibraryManager()
    manager.add_book("Test Title", "Test Author", "1234567890")
    manager.borrow_book("1234567890")
    assert not manager.inventory["1234567890"].is_available

def test_borrow_book_invalid_isbn():
    manager = LibraryManager()
    manager.borrow_book("1234567890")
    assert len(manager.inventory) == 0


def test_return_book_valid():
    manager = LibraryManager()
    manager.add_book("Test Title", "Test Author", "1234567890")
    manager.borrow_book("1234567890")
    manager.return_book("1234567890")
    assert manager.inventory["1234567890"].is_available

def test_return_book_invalid_isbn():
    manager = LibraryManager()
    manager.return_book("1234567890")
    assert len(manager.inventory) == 0


def test_show_inventory_empty():
    manager = LibraryManager()
    manager.show_inventory()

def test_show_inventory_non_empty():
    manager = LibraryManager()
    manager.add_book("Test Title", "Test Author", "1234567890")
    manager.show_inventory()