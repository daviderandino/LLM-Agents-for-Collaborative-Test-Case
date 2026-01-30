import pytest
from data.input_code.04_library import *

# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------
@pytest.fixture
def fresh_manager():
    """Provides a new LibraryManager instance for each test."""
    return LibraryManager()

# ----------------------------------------------------------------------
# Book.__str__ tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "title, author, isbn, is_available, expected",
    [
        ("1984", "George Orwell", "12345", True,
         "[Available] 1984 by George Orwell (ISBN: 12345)"),
        ("Brave New World", "Aldous Huxley", "67890", False,
         "[Borrowed] Brave New World by Aldous Huxley (ISBN: 67890)"),
    ]
)
def test_book_str(title, author, isbn, is_available, expected):
    book = Book(title, author, isbn)
    book.is_available = is_available
    assert str(book) == expected

# ----------------------------------------------------------------------
# LibraryManager.add_book tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "title, author, isbn, expected_stdout, expected_keys",
    [
        ("Dune", "Frank Herbert", "ABC123",
         "Success: Added 'Dune' to the library.\n", ["ABC123"]),
        ("Short ISBN", "Anon", "12",
         "[!] Error: ISBN '12' is too short.\n", []),
    ]
)
def test_add_book_basic(fresh_manager, title, author, isbn,
                        expected_stdout, expected_keys, capsys):
    fresh_manager.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out == expected_stdout
    assert list(fresh_manager.inventory.keys()) == expected_keys

def test_add_book_duplicate(fresh_manager, capsys):
    # First addition (should succeed)
    fresh_manager.add_book("Dune", "Frank Herbert", "ABC123")
    capsys.readouterr()  # clear

    # Attempt duplicate
    fresh_manager.add_book("Duplicate Dune", "Frank Herbert", "ABC123")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: A book with ISBN ABC123 already exists.\n"
    assert list(fresh_manager.inventory.keys()) == ["ABC123"]

# ----------------------------------------------------------------------
# LibraryManager.borrow_book tests
# ----------------------------------------------------------------------
def test_borrow_book_not_exist(fresh_manager, capsys):
    fresh_manager.borrow_book("NONEXIST")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: Book with ISBN NONEXIST not found.\n"
    assert fresh_manager.inventory == {}

def test_borrow_book_success(fresh_manager, capsys):
    fresh_manager.add_book("Dune", "Frank Herbert", "ABC123")
    capsys.readouterr()  # clear previous output

    fresh_manager.borrow_book("ABC123")
    captured = capsys.readouterr()
    assert captured.out == "Success: You have borrowed 'Dune'.\n"
    assert fresh_manager.inventory["ABC123"].is_available is False

def test_borrow_book_unavailable(fresh_manager, capsys):
    fresh_manager.add_book("Dune", "Frank Herbert", "ABC123")
    capsys.readouterr()
    # First borrow makes it unavailable
    fresh_manager.borrow_book("ABC123")
    capsys.readouterr()
    # Second attempt should hit unavailable branch
    fresh_manager.borrow_book("ABC123")
    captured = capsys.readouterr()
    assert captured.out == "[!] Unavailable: 'Dune' is currently borrowed by someone else.\n"
    assert fresh_manager.inventory["ABC123"].is_available is False

# ----------------------------------------------------------------------
# LibraryManager.return_book tests
# ----------------------------------------------------------------------
def test_return_book_not_exist(fresh_manager, capsys):
    fresh_manager.return_book("UNKNOWN")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: We do not own a book with ISBN UNKNOWN.\n"
    assert fresh_manager.inventory == {}

def test_return_book_success(fresh_manager, capsys):
    fresh_manager.add_book("Dune", "Frank Herbert", "ABC123")
    capsys.readouterr()
    fresh_manager.borrow_book("ABC123")
    capsys.readouterr()
    fresh_manager.return_book("ABC123")
    captured = capsys.readouterr()
    assert captured.out == "Success: 'Dune' has been returned.\n"
    assert fresh_manager.inventory["ABC123"].is_available is True

def test_return_book_already_available(fresh_manager, capsys):
    fresh_manager.add_book("Dune", "Frank Herbert", "ABC123")
    capsys.readouterr()
    fresh_manager.return_book("ABC123")
    captured = capsys.readouterr()
    assert captured.out == "[!] Strange: You are trying to return 'Dune', but it was already here.\n"
    assert fresh_manager.inventory["ABC123"].is_available is True

# ----------------------------------------------------------------------
# LibraryManager.show_inventory tests
# ----------------------------------------------------------------------
def test_show_inventory_empty(fresh_manager, capsys):
    fresh_manager.show_inventory()
    captured = capsys.readouterr()
    expected = (
        "\n--- Current Library Inventory ---\n"
        "The library is empty.\n"
        "---------------------------------\n\n"
    )
    assert captured.out == expected

def test_show_inventory_non_empty(fresh_manager, capsys):
    fresh_manager.add_book("Dune", "Frank Herbert", "ABC123")
    capsys.readouterr()
    fresh_manager.show_inventory()
    captured = capsys.readouterr()
    # The output should contain the string representation of the added book
    assert "[Available] Dune by Frank Herbert (ISBN: ABC123)" in captured.out