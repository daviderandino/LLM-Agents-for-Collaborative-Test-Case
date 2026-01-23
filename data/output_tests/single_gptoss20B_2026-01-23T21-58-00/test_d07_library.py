import pytest
from data.input_code.d07_library import Book, LibraryManager


def test_add_book_success_and_duplicate_and_short_isbn(capsys):
    manager = LibraryManager()

    # Successful addition
    manager.add_book("The Great Gatsby", "F. Scott Fitzgerald", "123")
    captured = capsys.readouterr()
    assert "Success: Added 'The Great Gatsby' to the library." in captured.out
    assert "123" in manager.inventory
    assert isinstance(manager.inventory["123"], Book)

    # Duplicate ISBN
    manager.add_book("Another Book", "Author", "123")
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 123 already exists." in captured.out
    # Inventory should still contain only the first book
    assert len(manager.inventory) == 1

    # ISBN too short
    manager.add_book("Short ISBN", "Author", "12")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out
    # Inventory unchanged
    assert len(manager.inventory) == 1


def test_borrow_book_success_and_unavailable_and_not_found(capsys):
    manager = LibraryManager()
    manager.add_book("1984", "George Orwell", "456")
    capsys.readouterr()  # clear output

    # Successful borrow
    manager.borrow_book("456")
    captured = capsys.readouterr()
    assert "Success: You have borrowed '1984'." in captured.out
    assert not manager.inventory["456"].is_available

    # Attempt to borrow again (unavailable)
    manager.borrow_book("456")
    captured = capsys.readouterr()
    assert "[!] Unavailable: '1984' is currently borrowed by someone else." in captured.out

    # Borrow non-existent book
    manager.borrow_book("999")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN 999 not found." in captured.out


def test_return_book_success_and_already_available_and_not_found(capsys):
    manager = LibraryManager()
    manager.add_book("Brave New World", "Aldous Huxley", "789")
    capsys.readouterr()  # clear output

    # Borrow first
    manager.borrow_book("789")
    capsys.readouterr()

    # Successful return
    manager.return_book("789")
    captured = capsys.readouterr()
    assert "Success: 'Brave New World' has been returned." in captured.out
    assert manager.inventory["789"].is_available

    # Attempt to return again (already available)
    manager.return_book("789")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'Brave New World', but it was already here." in captured.out

    # Return non-existent book
    manager.return_book("999")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN 999." in captured.out


def test_show_inventory_empty_and_nonempty(capsys):
    manager = LibraryManager()

    # Empty inventory
    manager.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

    # Add a book and show inventory
    manager.add_book("Fahrenheit 451", "Ray Bradbury", "321")
    capsys.readouterr()
    manager.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Fahrenheit 451 by Ray Bradbury (ISBN: 321)" in captured.out
    assert "---------------------------------" in captured.out


def test_book_str_and_default_availability():
    book = Book("Dune", "Frank Herbert", "111")
    # Default availability
    assert book.is_available is True
    expected_str = "[Available] Dune by Frank Herbert (ISBN: 111)"
    assert str(book) == expected_str

    # Change availability and test string
    book.is_available = False
    expected_str_borrowed = "[Borrowed] Dune by Frank Herbert (ISBN: 111)"
    assert str(book) == expected_str_borrowed