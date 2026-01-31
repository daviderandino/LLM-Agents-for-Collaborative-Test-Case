import pytest
from data.input_code.d04_library import *

# -------------------- add_book tests --------------------

@pytest.mark.parametrize(
    "title, author, isbn, expected_output, expected_keys",
    [
        ("Short ISBN", "A", "12",
         "[!] Error: ISBN '12' is too short.\n",
         []),
    ]
)
def test_add_book_validation_error(title, author, isbn, expected_output, expected_keys, capsys):
    manager = LibraryManager()
    manager.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out == expected_output
    assert list(manager.inventory.keys()) == expected_keys


def test_add_book_duplicate_detection(capsys):
    manager = LibraryManager()
    # prepopulate with a book
    manager.add_book("First Book", "B", "12345")
    # attempt to add duplicate
    manager.add_book("First Book", "B", "12345")
    captured = capsys.readouterr()
    # first call prints success, second prints error
    expected = "Success: Added 'First Book' to the library.\n[!] Error: A book with ISBN 12345 already exists.\n"
    assert captured.out == expected
    assert list(manager.inventory.keys()) == ["12345"]


def test_add_book_duplicate_branch(capsys):
    manager = LibraryManager()
    # prepopulate with a book
    manager.add_book("First Book", "B", "12345")
    # attempt duplicate addition
    manager.add_book("Second Book", "C", "12345")
    captured = capsys.readouterr()
    # only the duplicate error should be printed after the initial success
    expected = "Success: Added 'First Book' to the library.\n[!] Error: A book with ISBN 12345 already exists.\n"
    assert captured.out == expected
    # inventory unchanged
    assert list(manager.inventory.keys()) == ["12345"]


# -------------------- borrow_book tests --------------------

def test_borrow_book_not_found(capsys):
    manager = LibraryManager()
    manager.borrow_book("99999")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: Book with ISBN 99999 not found.\n"


def test_borrow_book_unavailable(capsys):
    manager = LibraryManager()
    # prepopulate a borrowed book
    borrowed = Book("Borrowed Book", "D", "11111")
    borrowed.is_available = False
    manager.inventory["11111"] = borrowed
    manager.borrow_book("11111")
    captured = capsys.readouterr()
    assert captured.out == "[!] Unavailable: 'Borrowed Book' is currently borrowed by someone else.\n"


def test_borrow_book_success(capsys):
    manager = LibraryManager()
    # prepopulate an available book
    manager.add_book("Available Book", "E", "22222")
    manager.borrow_book("22222")
    captured = capsys.readouterr()
    # first call prints success of addition, second prints borrow success
    expected = "Success: Added 'Available Book' to the library.\nSuccess: You have borrowed 'Available Book'.\n"
    assert captured.out == expected
    assert manager.inventory["22222"].is_available is False


# -------------------- return_book tests --------------------

def test_return_book_not_found(capsys):
    manager = LibraryManager()
    manager.return_book("33333")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: We do not own a book with ISBN 33333.\n"


def test_return_book_already_available(capsys):
    manager = LibraryManager()
    # prepopulate an available book
    manager.add_book("Already Here", "F", "44444")
    manager.return_book("44444")
    captured = capsys.readouterr()
    # addition success + strange message
    expected = "Success: Added 'Already Here' to the library.\n[!] Strange: You are trying to return 'Already Here', but it was already here.\n"
    assert captured.out == expected
    assert manager.inventory["44444"].is_available is True


def test_return_book_success(capsys):
    manager = LibraryManager()
    # prepopulate a borrowed book
    borrowed = Book("Returned Book", "G", "55555")
    borrowed.is_available = False
    manager.inventory["55555"] = borrowed
    manager.return_book("55555")
    captured = capsys.readouterr()
    assert captured.out == "Success: 'Returned Book' has been returned.\n"
    assert manager.inventory["55555"].is_available is True


# -------------------- show_inventory tests --------------------

def test_show_inventory_empty(capsys):
    manager = LibraryManager()
    manager.show_inventory()
    captured = capsys.readouterr()
    expected_lines = [
        "",                                 # blank line before header
        "--- Current Library Inventory ---",
        "The library is empty.",
        "---------------------------------",
        ""                                  # final blank line after footer
    ]
    assert captured.out.splitlines() == expected_lines


def test_show_inventory_non_empty(capsys):
    manager = LibraryManager()
    # add two books with different availability
    manager.add_book("Book One", "H", "66666")
    manager.add_book("Book Two", "I", "77777")
    # make second book borrowed
    manager.inventory["77777"].is_available = False
    manager.show_inventory()
    captured = capsys.readouterr()
    expected_lines = [
        "Success: Added 'Book One' to the library.",
        "Success: Added 'Book Two' to the library.",
        "",                                 # blank line before header
        "--- Current Library Inventory ---",
        "[Available] Book One by H (ISBN: 66666)",
        "[Borrowed] Book Two by I (ISBN: 77777)",
        "---------------------------------",
        ""                                  # final blank line after footer
    ]
    assert captured.out.splitlines() == expected_lines