import pytest
from data.input_code.d07_library import *

@pytest.mark.parametrize(
    "title, author, isbn, expected",
    [
        ("Book1", "Author1", "123456789", "Success: Added 'Book1' to the library."),
        ("Book2", "Author2", "12", "[!] Error: ISBN '12' is too short."),
        ("Book3", "Author3", "123456789", "Success: Added 'Book1' to the library.\n[!] Error: A book with ISBN 123456789 already exists."),
    ],
)
def test_add_book(title, author, isbn, expected, capsys):
    manager = LibraryManager()
    # For duplicate test, pre-add the book
    if isbn == "123456789" and title == "Book3":
        manager.add_book("Book1", "Author1", "123456789")
    manager.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected

@pytest.mark.parametrize(
    "isbn, expected",
    [
        ("123456789", "Success: Added 'Book1' to the library.\nSuccess: You have borrowed 'Book1'."),
        ("987654321", "[!] Error: Book with ISBN 987654321 not found."),
    ],
)
def test_borrow_book(isbn, expected, capsys):
    manager = LibraryManager()
    # Pre-add Book1 for first case
    if isbn == "123456789":
        manager.add_book("Book1", "Author1", "123456789")
    manager.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected

def test_borrow_book_already_borrowed(capsys):
    manager = LibraryManager()
    manager.add_book("Book1", "Author1", "123456789")
    # First borrow
    manager.borrow_book("123456789")
    # Second borrow attempt
    manager.borrow_book("123456789")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'Book1' to the library.\nSuccess: You have borrowed 'Book1'.\n[!] Unavailable: 'Book1' is currently borrowed by someone else."

@pytest.mark.parametrize(
    "isbn, expected",
    [
        ("123456789", "Success: Added 'Book1' to the library.\nSuccess: You have borrowed 'Book1'.\nSuccess: 'Book1' has been returned."),
        ("987654321", "[!] Error: We do not own a book with ISBN 987654321."),
    ],
)
def test_return_book(isbn, expected, capsys):
    manager = LibraryManager()
    if isbn == "123456789":
        manager.add_book("Book1", "Author1", "123456789")
        manager.borrow_book("123456789")
    manager.return_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected

def test_return_book_already_available(capsys):
    manager = LibraryManager()
    manager.add_book("Book1", "Author1", "123456789")
    # Return before borrowing
    manager.return_book("123456789")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'Book1' to the library.\n[!] Strange: You are trying to return 'Book1', but it was already here."

def test_show_inventory_empty(capsys):
    manager = LibraryManager()
    manager.show_inventory()
    captured = capsys.readouterr()
    expected = (
        "\n--- Current Library Inventory ---\n"
        "The library is empty.\n"
        "---------------------------------\n"
        "\n"
    )
    assert captured.out == expected

def test_show_inventory_non_empty(capsys):
    manager = LibraryManager()
    manager.add_book("Book1", "Author1", "123456789")
    manager.show_inventory()
    captured = capsys.readouterr()
    expected = (
        "Success: Added 'Book1' to the library.\n\n"
        "--- Current Library Inventory ---\n"
        "[Available] Book1 by Author1 (ISBN: 123456789)\n"
        "---------------------------------\n"
        "\n"
    )
    assert captured.out == expected