import pytest
from data.input_code.d07_library import *

# ---------- Book tests ----------
@pytest.mark.parametrize(
    "title, author, isbn, expected_str",
    [
        (
            "Test Book",
            "Test Author",
            "1234567890",
            "[Available] Test Book by Test Author (ISBN: 1234567890)",
        )
    ],
)
def test_book_init_and_str(title, author, isbn, expected_str):
    # Test __init__
    book = Book(title, author, isbn)
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn
    assert book.is_available is True

    # Test __str__
    assert str(book) == expected_str


# ---------- LibraryManager tests ----------
@pytest.fixture
def empty_manager():
    """Provides a fresh LibraryManager instance."""
    return LibraryManager()


def test_library_manager_workflow(empty_manager, capsys):
    manager = empty_manager

    # ---- T4: Add a valid book ----
    manager.add_book("Test Book", "Test Author", "1234567890")
    out = capsys.readouterr().out
    assert "Success: Added 'Test Book' to the library." in out
    assert "1234567890" in manager.inventory
    book = manager.inventory["1234567890"]
    assert isinstance(book, Book)
    assert book.is_available is True

    # ---- T5: Add a book with short ISBN (should be ignored) ----
    manager.add_book("Short ISBN Book", "Author", "12")
    out = capsys.readouterr().out
    assert "Error: ISBN '12' is too short." in out
    assert "12" not in manager.inventory

    # ---- T6: Add a duplicate ISBN (should be ignored) ----
    manager.add_book("Duplicate Book", "Author", "1234567890")
    out = capsys.readouterr().out
    assert "Error: A book with ISBN 1234567890 already exists." in out
    # inventory size unchanged
    assert len(manager.inventory) == 1

    # ---- T7: Borrow the available book ----
    manager.borrow_book("1234567890")
    out = capsys.readouterr().out
    assert "Success: You have borrowed 'Test Book'." in out
    assert book.is_available is False

    # ---- T8: Borrow the same book again (unavailable) ----
    manager.borrow_book("1234567890")
    out = capsys.readouterr().out
    assert "Unavailable: 'Test Book' is currently borrowed" in out
    assert book.is_available is False

    # ---- T9: Borrow a non‑existent book ----
    manager.borrow_book("9876543210")
    out = capsys.readouterr().out
    assert "Error: Book with ISBN 9876543210 not found." in out

    # ---- T10: Return the borrowed book ----
    manager.return_book("1234567890")
    out = capsys.readouterr().out
    assert "Success: 'Test Book' has been returned." in out
    assert book.is_available is True

    # ---- T11: Return the same book again (already available) ----
    manager.return_book("1234567890")
    out = capsys.readouterr().out
    assert "Strange: You are trying to return 'Test Book', but it was already here." in out
    assert book.is_available is True

    # ---- T12: Return a non‑existent book ----
    manager.return_book("9876543210")
    out = capsys.readouterr().out
    assert "Error: We do not own a book with ISBN 9876543210." in out

    # ---- T13: Show inventory when empty (use a fresh manager) ----
    fresh_manager = LibraryManager()
    fresh_manager.show_inventory()
    out = capsys.readouterr().out
    assert "The library is empty." in out

    # ---- T14: Show inventory when non‑empty ----
    fresh_manager.add_book("Another Book", "Another Author", "111222333")
    fresh_manager.show_inventory()
    out = capsys.readouterr().out
    assert "[Available] Another Book by Another Author (ISBN: 111222333)" in out