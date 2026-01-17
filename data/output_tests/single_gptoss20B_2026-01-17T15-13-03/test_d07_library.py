import pytest
from data.input_code.d07_library import Book, LibraryManager


def test_book_str_available_and_borrowed():
    book = Book("1984", "George Orwell", "12345")
    assert str(book) == "[Available] 1984 by George Orwell (ISBN: 12345)"
    book.is_available = False
    assert str(book) == "[Borrowed] 1984 by George Orwell (ISBN: 12345)"


@pytest.mark.parametrize(
    "isbn,expected_output,expected_inventory_size",
    [
        ("12", "[!] Error: ISBN '12' is too short.\n", 0),  # too short
        ("123", "Success: Added 'The Hobbit' to the library.\n", 1),  # valid
        ("123", "[!] Error: A book with ISBN 123 already exists.\n", 1),  # duplicate
    ],
)
def test_add_book(capsys, isbn, expected_output, expected_inventory_size):
    manager = LibraryManager()
    # Add first book if isbn is valid
    if isbn == "123":
        manager.add_book("The Hobbit", "J.R.R. Tolkien", isbn)
    # Now test the scenario
    manager.add_book("The Hobbit", "J.R.R. Tolkien", isbn)
    captured = capsys.readouterr()
    assert captured.out == expected_output
    assert len(manager.inventory) == expected_inventory_size
    if expected_inventory_size == 1:
        assert isbn in manager.inventory
        assert manager.inventory[isbn].title == "The Hobbit"








def test_inventory_integrity_and_duplicate_handling():
    manager = LibraryManager()
    manager.add_book("Unique Book", "Unique Author", "UNI")
    assert len(manager.inventory) == 1
    assert "UNI" in manager.inventory
    # Attempt to add duplicate
    manager.add_book("Duplicate Book", "Duplicate Author", "UNI")
    # Inventory should still have only one book
    assert len(manager.inventory) == 1
    # The book should remain the original
    assert manager.inventory["UNI"].title == "Unique Book"


def test_add_book_with_boundary_isbn_lengths(capsys):
    manager = LibraryManager()
    # ISBN length exactly 3 (boundary)
    manager.add_book("Boundary Book", "Boundary Author", "123")
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Boundary Book' to the library.\n"
    assert len(manager.inventory) == 1

    # ISBN length 2 (just below boundary)
    manager.add_book("Too Short", "Author", "12")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: ISBN '12' is too short.\n"
    assert len(manager.inventory) == 1  # still only the first book


def test_borrow_and_return_toggle_is_available():
    manager = LibraryManager()
    manager.add_book("Toggle Book", "Toggle Author", "TOG")
    # Initially available
    assert manager.inventory["TOG"].is_available
    # Borrow
    manager.borrow_book("TOG")
    assert not manager.inventory["TOG"].is_available
    # Return
    manager.return_book("TOG")
    assert manager.inventory["TOG"].is_available
    # Borrow again
    manager.borrow_book("TOG")
    assert not manager.inventory["TOG"].is_available
    # Return again
    manager.return_book("TOG")
    assert manager.inventory["TOG"].is_available