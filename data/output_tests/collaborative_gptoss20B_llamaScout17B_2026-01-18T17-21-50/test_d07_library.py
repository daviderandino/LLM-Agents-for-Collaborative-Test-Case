import pytest
from data.input_code.d07_library import *

def test_show_inventory_empty():
    manager = LibraryManager()
    manager.show_inventory()
    # No direct assert, but visually verify output

def test_add_book_success():
    manager = LibraryManager()
    manager.add_book("Book1", "Author1", "123")
    assert "123" in manager.inventory

def test_add_book_duplicate():
    manager = LibraryManager()
    manager.add_book("Book1", "Author1", "123")
    manager.add_book("Book2", "Author2", "123")
    # No direct assert, but visually verify output

def test_add_book_isbn_too_short():
    manager = LibraryManager()
    manager.add_book("Book1", "Author1", "12")
    # No direct assert, but visually verify output

def test_add_book_empty_isbn():
    manager = LibraryManager()
    manager.add_book("Book1", "Author1", "")
    # No direct assert, but visually verify output

def test_add_book_isbn_none():
    manager = LibraryManager()
    with pytest.raises(TypeError):
        manager.add_book("Book1", "Author1", None)

def test_borrow_book_success():
    manager = LibraryManager()
    manager.add_book("Book1", "Author1", "123")
    manager.borrow_book("123")
    assert not manager.inventory["123"].is_available

def test_borrow_book_already_borrowed():
    manager = LibraryManager()
    manager.add_book("Book1", "Author1", "123")
    manager.borrow_book("123")
    manager.borrow_book("123")
    # No direct assert, but visually verify output

def test_borrow_book_non_existent():
    manager = LibraryManager()
    manager.borrow_book("999")
    # No direct assert, but visually verify output

def test_return_book_success():
    manager = LibraryManager()
    manager.add_book("Book1", "Author1", "123")
    manager.borrow_book("123")
    manager.return_book("123")
    assert manager.inventory["123"].is_available

def test_return_book_already_available():
    manager = LibraryManager()
    manager.add_book("Book1", "Author1", "123")
    manager.return_book("123")
    # No direct assert, but visually verify output

def test_return_book_non_existent():
    manager = LibraryManager()
    manager.return_book("999")
    # No direct assert, but visually verify output

def test_show_inventory_non_empty():
    manager = LibraryManager()
    manager.add_book("Book1", "Author1", "123")
    manager.show_inventory()
    # No direct assert, but visually verify output