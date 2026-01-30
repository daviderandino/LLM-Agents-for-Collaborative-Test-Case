import pytest
from data.input_code.04_library import *

@pytest.mark.parametrize(
    "title, author, isbn, expected_stdout, expected_size, expected_book",
    [
        # T1: ISBN too short
        (
            "Tiny",
            "A",
            "12",
            "[!] Error: ISBN '12' is too short.",
            0,
            None,
        ),
        # T2: Successful add
        (
            "Python 101",
            "Guido",
            "12345",
            "Success: Added 'Python 101' to the library.",
            1,
            {"title": "Python 101", "author": "Guido", "isbn": "12345", "is_available": True},
        ),
    ],
)
def test_add_book(title, author, isbn, expected_stdout, expected_size, expected_book, capsys):
    manager = LibraryManager()
    # For T2, we need to ensure no prior books
    manager.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert expected_stdout in captured.out
    assert len(manager.inventory) == expected_size
    if expected_book:
        book = manager.inventory[isbn]
        assert book.title == expected_book["title"]
        assert book.author == expected_book["author"]
        assert book.isbn == expected_book["isbn"]
        assert book.is_available == expected_book["is_available"]

def test_add_duplicate(capsys):
    manager = LibraryManager()
    # Setup previous book
    manager.add_book("Python 101", "Guido", "12345")
    # Attempt duplicate
    manager.add_book("Another", "Someone", "12345")
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 12345 already exists." in captured.out
    assert len(manager.inventory) == 1

@pytest.mark.parametrize(
    "isbn, expected_stdout",
    [
        ("99999", "[!] Error: Book with ISBN 99999 not found."),
    ],
)
def test_borrow_nonexistent(isbn, expected_stdout, capsys):
    manager = LibraryManager()
    manager.borrow_book(isbn)
    captured = capsys.readouterr()
    assert expected_stdout in captured.out

def test_borrow_success(capsys):
    manager = LibraryManager()
    manager.add_book("Python 101", "Guido", "12345")
    manager.borrow_book("12345")
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'Python 101'." in captured.out
    assert not manager.inventory["12345"].is_available

def test_borrow_already_borrowed(capsys):
    manager = LibraryManager()
    manager.add_book("Python 101", "Guido", "12345")
    # Manually set as borrowed
    manager.inventory["12345"].is_available = False
    manager.borrow_book("12345")
    captured = capsys.readouterr()
    assert "[!] Unavailable: 'Python 101' is currently borrowed by someone else." in captured.out

@pytest.mark.parametrize(
    "isbn, expected_stdout",
    [
        ("00000", "[!] Error: We do not own a book with ISBN 00000."),
    ],
)
def test_return_nonexistent(isbn, expected_stdout, capsys):
    manager = LibraryManager()
    manager.return_book(isbn)
    captured = capsys.readouterr()
    assert expected_stdout in captured.out

def test_return_already_available(capsys):
    manager = LibraryManager()
    manager.add_book("New Book", "Writer", "67890")
    manager.return_book("67890")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'New Book', but it was already here." in captured.out

def test_return_success(capsys):
    manager = LibraryManager()
    manager.add_book("Python 101", "Guido", "12345")
    # Borrow first
    manager.borrow_book("12345")
    # Return
    manager.return_book("12345")
    captured = capsys.readouterr()
    assert "Success: 'Python 101' has been returned." in captured.out
    assert manager.inventory["12345"].is_available

def test_show_inventory_empty(capsys):
    manager = LibraryManager()
    manager.show_inventory()
    captured = capsys.readouterr()
    assert "--- Current Library Inventory ---" in captured.out
    assert "The library is empty." in captured.out
    assert "---------------------------------" in captured.out

def test_show_inventory_nonempty(capsys):
    manager = LibraryManager()
    manager.add_book("Python 101", "Guido", "12345")
    manager.add_book("New Book", "Writer", "67890")
    # Borrow one
    manager.borrow_book("12345")
    manager.show_inventory()
    captured = capsys.readouterr()
    assert "--- Current Library Inventory ---" in captured.out
    assert "[Borrowed] Python 101 by Guido (ISBN: 12345)" in captured.out
    assert "[Available] New Book by Writer (ISBN: 67890)" in captured.out
    assert "---------------------------------" in captured.out