import pytest
from data.input_code.d07_library import *

@pytest.mark.parametrize(
    "title, author, isbn",
    [("Test Book", "Author", "123")]
)
def test_T1_BookInit(title, author, isbn):
    book = Book(title, author, isbn)
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn
    assert book.is_available is True

def test_T2_BookStr():
    book = Book("Test Book", "Author", "123")
    expected_str = "[Available] Test Book by Author (ISBN: 123)"
    assert str(book) == expected_str

def test_T3_AddBookShortISBN():
    manager = LibraryManager()
    manager.add_book("Short ISBN Book", "Author", "12")
    # Inventory should remain empty
    assert len(manager.inventory) == 0

def test_T4_AddBookDuplicate():
    manager = LibraryManager()
    manager.add_book("Original Book", "Author", "123")
    assert len(manager.inventory) == 1
    manager.add_book("Duplicate Book", "Author", "123")
    # Duplicate should not be added
    assert len(manager.inventory) == 1

def test_T5_AddBookNormal():
    manager = LibraryManager()
    manager.add_book("Normal Book", "Author", "456")
    assert "456" in manager.inventory
    book = manager.inventory["456"]
    assert book.title == "Normal Book"
    assert book.author == "Author"
    assert book.isbn == "456"
    assert book.is_available is True

def test_T6_BorrowNonExisting():
    manager = LibraryManager()
    # Borrowing a non-existing book should not raise an exception
    manager.borrow_book("999")

def test_T7_BorrowAvailable():
    manager = LibraryManager()
    manager.add_book("Normal Book", "Author", "456")
    manager.borrow_book("456")
    book = manager.inventory["456"]
    assert book.is_available is False

def test_T8_BorrowAlreadyBorrowed():
    manager = LibraryManager()
    manager.add_book("Normal Book", "Author", "456")
    manager.borrow_book("456")  # First borrow
    manager.borrow_book("456")  # Second borrow attempt
    book = manager.inventory["456"]
    assert book.is_available is False

def test_T9_ReturnNonExisting():
    manager = LibraryManager()
    # Returning a non-existing book should not raise an exception
    manager.return_book("999")

def test_T10_ReturnAlreadyAvailable():
    manager = LibraryManager()
    manager.add_book("Normal Book", "Author", "456")
    manager.borrow_book("456")   # Borrow to make it unavailable
    manager.return_book("456")   # Return to make it available
    # Now the book is available; attempting to return again triggers the "Strange" branch
    manager.return_book("456")
    book = manager.inventory["456"]
    assert book.is_available is True

def test_T11_ReturnBorrowed():
    manager = LibraryManager()
    manager.add_book("Normal Book", "Author", "456")
    manager.borrow_book("456")   # Borrow
    manager.return_book("456")   # Return
    book = manager.inventory["456"]
    assert book.is_available is True

def test_T12_ShowInventoryEmpty():
    manager = LibraryManager()
    # Should not raise any exception
    manager.show_inventory()

def test_T13_ShowInventoryNonEmpty():
    manager = LibraryManager()
    manager.add_book("Normal Book", "Author", "456")
    # Should not raise any exception
    manager.show_inventory()