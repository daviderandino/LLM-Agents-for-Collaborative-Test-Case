import pytest
from data.input_code.d04_library import *

# ------------------- Book.__str__ tests ------------------- #
@pytest.mark.parametrize(
    "is_available, expected",
    [
        (True, "[Available] Test Book by Test Author (ISBN: 12345)"),
        (False, "[Borrowed] Test Book by Test Author (ISBN: 12345)"),
    ],
)
def test_book_str(is_available, expected):
    book = Book(title="Test Book", author="Test Author", isbn="12345")
    book.is_available = is_available
    assert str(book) == expected


# ------------------- LibraryManager.add_book tests ------------------- #
@pytest.mark.parametrize(
    "title, author, isbn, prepopulate, expected_output, expect_exception",
    [
        # Short ISBN
        ("Short ISBN Book", "Author", "12", False,
         "[!] Error: ISBN '12' is too short.", False),
        # Duplicate ISBN
        ("Duplicate Book", "Author", "123", True,
         "[!] Error: A book with ISBN 123 already exists.", False),
        # Normal add
        ("Normal Book", "Author", "123", False,
         "Success: Added 'Normal Book' to the library.", False),
        # None ISBN triggers TypeError
        ("None ISBN Book", "Author", None, False,
         "", True),
    ],
)
def test_add_book(title, author, isbn, prepopulate, expected_output, expect_exception, capsys):
    manager = LibraryManager()
    if prepopulate:
        # add a book first so that the next add triggers duplicate detection
        manager.add_book("Existing", "Author", isbn)
        # clear the output from the prepopulation step
        capsys.readouterr()

    if expect_exception:
        with pytest.raises(TypeError):
            manager.add_book(title, author, isbn)
    else:
        manager.add_book(title, author, isbn)
        captured = capsys.readouterr()
        # The method prints a newline after each message; we compare stripped lines
        assert captured.out.strip() == expected_output.strip()


# ------------------- LibraryManager.borrow_book tests ------------------- #
def test_borrow_book_nonexistent(capsys):
    manager = LibraryManager()
    manager.borrow_book("999")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: Book with ISBN 999 not found."


def test_borrow_book_flow(capsys):
    manager = LibraryManager()
    # add a normal book first
    manager.add_book("Normal Book", "Author", "123")
    capsys.readouterr()  # clear output

    # borrow the available book
    manager.borrow_book("123")
    out1 = capsys.readouterr().out.strip()
    assert out1 == "Success: You have borrowed 'Normal Book'."

    # attempt to borrow again (already borrowed)
    manager.borrow_book("123")
    out2 = capsys.readouterr().out.strip()
    assert out2 == "[!] Unavailable: 'Normal Book' is currently borrowed by someone else."


# ------------------- LibraryManager.return_book tests ------------------- #
def test_return_book_nonexistent(capsys):
    manager = LibraryManager()
    manager.return_book("999")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: We do not own a book with ISBN 999."


def test_return_book_flow(capsys):
    manager = LibraryManager()
    manager.add_book("Normal Book", "Author", "123")
    capsys.readouterr()  # clear

    # borrow first to set status to borrowed
    manager.borrow_book("123")
    capsys.readouterr()  # clear

    # return the borrowed book (success)
    manager.return_book("123")
    out_success = capsys.readouterr().out.strip()
    assert out_success == "Success: 'Normal Book' has been returned."

    # attempt to return again (already returned)
    manager.return_book("123")
    out_strange = capsys.readouterr().out.strip()
    assert out_strange == "[!] Strange: You are trying to return 'Normal Book', but it was already here."


# ------------------- LibraryManager.show_inventory tests ------------------- #
def test_show_inventory_empty(capsys):
    manager = LibraryManager()
    manager.show_inventory()
    captured = capsys.readouterr().out
    # The method prints a header/footer plus the empty message
    assert "The library is empty." in captured
    assert "--- Current Library Inventory ---" in captured
    assert "---------------------------------" in captured


def test_show_inventory_nonempty(capsys):
    manager = LibraryManager()
    manager.add_book("Normal Book", "Author", "123")
    capsys.readouterr()  # clear
    manager.show_inventory()
    captured = capsys.readouterr().out
    # Verify that the book representation appears in the output
    assert "[Available] Normal Book by Author (ISBN: 123)" in captured
    assert "--- Current Library Inventory ---" in captured
    assert "---------------------------------" in captured