import pytest
from data.input_code.d07_library import *


@pytest.fixture
def lib():
    """Provide a fresh LibraryManager for each test."""
    return LibraryManager()


# -------------------- add_book tests --------------------
@pytest.mark.parametrize(
    "title, author, isbn, expected",
    [
        ("Short ISBN Book", "Author A", "12",
         "[!] Error: ISBN '12' is too short."),
        ("New Book", "Author D", "456",
         "Success: Added 'New Book' to the library."),
    ]
)
def test_add_book_simple(lib, title, author, isbn, expected, capsys):
    """Test adding a book with short ISBN and a successful addition."""
    lib.add_book(title, author, isbn)
    captured = capsys.readouterr().out.strip()
    assert captured == expected


def test_add_book_duplicate(lib, capsys):
    """Test adding a duplicate ISBN."""
    # first addition (should succeed)
    lib.add_book("First Book", "Author B", "123")
    capsys.readouterr()  # clear previous output
    # duplicate addition
    lib.add_book("Duplicate Book", "Author C", "123")
    captured = capsys.readouterr().out.strip()
    assert captured == "[!] Error: A book with ISBN 123 already exists."


# -------------------- borrow_book tests --------------------
@pytest.mark.parametrize(
    "isbn, expected",
    [
        ("999", "[!] Error: Book with ISBN 999 not found."),
        ("101", "Success: You have borrowed 'Borrowable Book'."),
    ]
)
def test_borrow_book_simple(lib, isbn, expected, capsys):
    """Test borrowing a non‑existent book and a successful borrow."""
    if isbn == "101":
        lib.add_book("Borrowable Book", "Author F", "101")
        capsys.readouterr()  # clear output from add_book
    lib.borrow_book(isbn)
    captured = capsys.readouterr().out.strip()
    assert captured == expected


def test_borrow_book_unavailable(lib, capsys):
    """Test borrowing a book that is already borrowed."""
    lib.add_book("Borrowed Book", "Author E", "789")
    capsys.readouterr()  # clear output
    lib.borrow_book("789")  # first borrow – makes it unavailable
    capsys.readouterr()  # clear output
    lib.borrow_book("789")  # second attempt
    captured = capsys.readouterr().out.strip()
    assert captured == "[!] Unavailable: 'Borrowed Book' is currently borrowed by someone else."


# -------------------- return_book tests --------------------
@pytest.mark.parametrize(
    "isbn, expected",
    [
        ("888", "[!] Error: We do not own a book with ISBN 888."),
        ("202", "[!] Strange: You are trying to return 'Returnable Book', but it was already here."),
    ]
)
def test_return_book_simple(lib, isbn, expected, capsys):
    """Test returning a non‑existent book and returning an already available book."""
    if isbn == "202":
        lib.add_book("Returnable Book", "Author G", "202")
        capsys.readouterr()  # clear output from add_book
    lib.return_book(isbn)
    captured = capsys.readouterr().out.strip()
    assert captured == expected


def test_return_book_success(lib, capsys):
    """Test a successful return operation."""
    lib.add_book("Returned Book", "Author H", "303")
    capsys.readouterr()  # clear output
    lib.borrow_book("303")
    capsys.readouterr()  # clear output
    lib.return_book("303")
    captured = capsys.readouterr().out.strip()
    assert captured == "Success: 'Returned Book' has been returned."


# -------------------- show_inventory tests --------------------
@pytest.mark.parametrize(
    "setup_actions, expected_lines",
    [
        # Empty inventory
        ([], [
            "",
            "--- Current Library Inventory ---",
            "The library is empty.",
            "---------------------------------",
            ""
        ]),
        # Inventory with one book
        ([
            ("add_book", {"title": "Inventory Book", "author": "Author I", "isbn": "404"})
        ], [
            "",
            "--- Current Library Inventory ---",
            "[Available] Inventory Book by Author I (ISBN: 404)",
            "---------------------------------",
            ""
        ]),
    ]
)
def test_show_inventory(lib, setup_actions, expected_lines, capsys):
    """Test inventory display for empty and non‑empty states."""
    for method_name, kwargs in setup_actions:
        getattr(lib, method_name)(**kwargs)
        capsys.readouterr()  # discard any intermediate output
    lib.show_inventory()
    captured = capsys.readouterr().out.splitlines()
    assert captured == expected_lines