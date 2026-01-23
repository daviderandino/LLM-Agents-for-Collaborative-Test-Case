import pytest
from data.input_code.d07_library import *

@pytest.fixture
def manager():
    return LibraryManager()

@pytest.mark.parametrize(
    "title,author,isbn,expected_size,expected_isbn,expected_available",
    [
        ("Book1", "Author1", "123", 1, "123", True),   # T1
        ("Book2", "Author2", "12", 0, None, None),     # T2
        ("Book1", "Author1", "123", 1, None, None),    # T3
    ]
)
def test_add_book(manager, title, author, isbn, expected_size, expected_isbn, expected_available):
    manager.add_book(title, author, isbn)
    assert len(manager.inventory) == expected_size
    # Only perform detailed checks when an ISBN is explicitly expected
    if expected_size == 1 and expected_isbn is not None:
        book = manager.inventory[expected_isbn]
        assert book.isbn == expected_isbn
        assert book.is_available == expected_available

def test_borrow_nonexistent(manager):
    manager.borrow_book("999")  # T4
    assert len(manager.inventory) == 0

def test_borrow_already_borrowed(manager):
    manager.add_book("Book1", "Author1", "123")
    manager.borrow_book("123")  # first borrow
    manager.borrow_book("123")  # T5
    assert len(manager.inventory) == 1
    assert not manager.inventory["123"].is_available

def test_borrow_available(manager):
    manager.add_book("Book1", "Author1", "123")
    manager.borrow_book("123")  # T6
    assert len(manager.inventory) == 1
    assert not manager.inventory["123"].is_available

def test_return_nonexistent(manager):
    manager.return_book("999")  # T7
    assert len(manager.inventory) == 0

def test_return_already_available(manager):
    manager.add_book("Book1", "Author1", "123")
    manager.return_book("123")  # T8
    assert len(manager.inventory) == 1
    assert manager.inventory["123"].is_available

def test_return_borrowed(manager):
    manager.add_book("Book1", "Author1", "123")
    manager.borrow_book("123")
    manager.return_book("123")  # T9
    assert len(manager.inventory) == 1
    assert manager.inventory["123"].is_available

def test_show_inventory_empty(manager):
    manager.show_inventory()  # T10
    assert len(manager.inventory) == 0

def test_show_inventory_not_empty(manager):
    manager.add_book("Book1", "Author1", "123")
    manager.show_inventory()  # T11
    assert len(manager.inventory) == 1

def test_book_str_borrowed():
    book = Book("Book1", "Author1", "123")
    book.is_available = False
    assert str(book) == "[Borrowed] Book1 by Author1 (ISBN: 123)"

import pytest
from data.input_code.d07_library import *

def test_book_str_available():
    book = Book("Book1", "Author1", "123")
    book.is_available = True
    assert str(book) == "[Available] Book1 by Author1 (ISBN: 123)"

import pytest
from data.input_code.d07_library import *

@pytest.mark.parametrize(
    "title,author,isbn,expected_msg",
    [
        ("Book1", "Author1", "12", "[!] Error: ISBN '12' is too short."),  # short ISBN
        ("Book1", "Author1", "123", "Success: Added 'Book1' to the library."),  # valid ISBN
    ],
)
def test_add_book_messages(manager, capsys, title, author, isbn, expected_msg):
    manager.add_book(title, author, isbn)
    out, _ = capsys.readouterr()
    assert expected_msg in out
    # Verify inventory size changes only on successful add
    if "Success" in expected_msg:
        assert len(manager.inventory) == 1
        assert manager.inventory[isbn].title == title
    else:
        assert len(manager.inventory) == 0

def test_add_book_duplicate_message(manager, capsys):
    manager.add_book("Book1", "Author1", "123")
    manager.add_book("Book1", "Author1", "123")  # duplicate
    out, _ = capsys.readouterr()
    assert "[!] Error: A book with ISBN 123 already exists." in out
    assert len(manager.inventory) == 1  # still only one book

@pytest.mark.parametrize(
    "isbn,expected_msg",
    [
        ("999", "[!] Error: Book with ISBN 999 not found."),  # nonexistent borrow
        ("123", "[!] Unavailable: 'Book1' is currently borrowed by someone else."),  # already borrowed
    ],
)
def test_borrow_book_messages(manager, capsys, isbn, expected_msg):
    # Setup
    if isbn == "123":
        manager.add_book("Book1", "Author1", "123")
        manager.borrow_book("123")  # first borrow
    manager.borrow_book(isbn)
    out, _ = capsys.readouterr()
    assert expected_msg in out
    # Inventory size unchanged
    assert len(manager.inventory) == (1 if isbn == "123" else 0)

def test_borrow_book_success_message(manager, capsys):
    manager.add_book("Book1", "Author1", "123")
    manager.borrow_book("123")
    out, _ = capsys.readouterr()
    assert "Success: You have borrowed 'Book1'." in out
    assert not manager.inventory["123"].is_available

@pytest.mark.parametrize(
    "isbn,expected_msg",
    [
        ("999", "[!] Error: We do not own a book with ISBN 999."),  # nonexistent return
        ("123", "[!] Strange: You are trying to return 'Book1', but it was already here."),  # already available
    ],
)
def test_return_book_messages(manager, capsys, isbn, expected_msg):
    # Setup
    if isbn == "123":
        manager.add_book("Book1", "Author1", "123")
    manager.return_book(isbn)
    out, _ = capsys.readouterr()
    assert expected_msg in out
    # Inventory size unchanged
    assert len(manager.inventory) == (1 if isbn == "123" else 0)

def test_return_book_success_message(manager, capsys):
    manager.add_book("Book1", "Author1", "123")
    manager.borrow_book("123")
    manager.return_book("123")
    out, _ = capsys.readouterr()
    assert "Success: 'Book1' has been returned." in out
    assert manager.inventory["123"].is_available

def test_show_inventory_empty_output(manager, capsys):
    manager.show_inventory()
    out, _ = capsys.readouterr()
    assert "--- Current Library Inventory ---" in out
    assert "The library is empty." in out
    assert "---------------------------------" in out

def test_show_inventory_not_empty_output(manager, capsys):
    manager.add_book("Book1", "Author1", "123")
    manager.show_inventory()
    out, _ = capsys.readouterr()
    assert "--- Current Library Inventory ---" in out
    assert "[Available] Book1 by Author1 (ISBN: 123)" in out
    assert "---------------------------------" in out