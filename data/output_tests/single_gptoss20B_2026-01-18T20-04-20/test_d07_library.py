import pytest

from data.input_code.d07_library import Book, LibraryManager


def test_book_str_default_available():
    book = Book("1984", "George Orwell", "1234567890")
    expected = "[Available] 1984 by George Orwell (ISBN: 1234567890)"
    assert str(book) == expected
    assert book.is_available is True


def test_book_str_after_borrow_and_return():
    book = Book("Brave New World", "Aldous Huxley", "0987654321")
    # Borrow the book
    book.is_available = False
    assert str(book) == "[Borrowed] Brave New World by Aldous Huxley (ISBN: 0987654321)"
    # Return the book
    book.is_available = True
    assert str(book) == "[Available] Brave New World by Aldous Huxley (ISBN: 0987654321)"


def test_library_manager_initial_state():
    lm = LibraryManager()
    assert isinstance(lm.inventory, dict)
    assert lm.inventory == {}


def test_add_book_success_and_inventory_update(capsys):
    lm = LibraryManager()
    lm.add_book("The Hobbit", "J.R.R. Tolkien", "ISBN001")
    captured = capsys.readouterr()
    assert "Success: Added 'The Hobbit' to the library." in captured.out
    assert "ISBN001" in lm.inventory
    assert isinstance(lm.inventory["ISBN001"], Book)
    assert lm.inventory["ISBN001"].title == "The Hobbit"
    assert lm.inventory["ISBN001"].author == "J.R.R. Tolkien"
    assert lm.inventory["ISBN001"].isbn == "ISBN001"
    assert lm.inventory["ISBN001"].is_available is True


def test_add_book_short_isbn(capsys):
    lm = LibraryManager()
    lm.add_book("Short ISBN", "Author", "12")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out
    assert lm.inventory == {}


def test_add_book_duplicate(capsys):
    lm = LibraryManager()
    lm.add_book("First Book", "Author A", "DUPLICATE")
    captured1 = capsys.readouterr()
    assert "Success: Added 'First Book' to the library." in captured1.out
    lm.add_book("Second Book", "Author B", "DUPLICATE")
    captured2 = capsys.readouterr()
    assert "[!] Error: A book with ISBN DUPLICATE already exists." in captured2.out
    # Inventory should still contain only the first book
    assert len(lm.inventory) == 1
    assert lm.inventory["DUPLICATE"].title == "First Book"


def test_borrow_book_success(capsys):
    lm = LibraryManager()
    lm.add_book("Book to Borrow", "Author", "BORROW1")
    lm.borrow_book("BORROW1")
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'Book to Borrow'." in captured.out
    assert lm.inventory["BORROW1"].is_available is False


def test_borrow_book_not_found(capsys):
    lm = LibraryManager()
    lm.borrow_book("NONEXISTENT")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN NONEXISTENT not found." in captured.out


def test_borrow_book_unavailable(capsys):
    lm = LibraryManager()
    lm.add_book("Borrowed Book", "Author", "UNAVAIL")
    lm.borrow_book("UNAVAIL")  # First borrow
    captured1 = capsys.readouterr()
    assert "Success: You have borrowed 'Borrowed Book'." in captured1.out
    lm.borrow_book("UNAVAIL")  # Second borrow attempt
    captured2 = capsys.readouterr()
    assert "[!] Unavailable: 'Borrowed Book' is currently borrowed by someone else." in captured2.out
    assert lm.inventory["UNAVAIL"].is_available is False


def test_return_book_success(capsys):
    lm = LibraryManager()
    lm.add_book("Returnable Book", "Author", "RETURN1")
    lm.borrow_book("RETURN1")
    lm.return_book("RETURN1")
    captured = capsys.readouterr()
    assert "Success: 'Returnable Book' has been returned." in captured.out
    assert lm.inventory["RETURN1"].is_available is True


def test_return_book_not_found(capsys):
    lm = LibraryManager()
    lm.return_book("MISSING")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN MISSING." in captured.out


def test_return_book_already_available(capsys):
    lm = LibraryManager()
    lm.add_book("Already Available", "Author", "ALREADY")
    lm.return_book("ALREADY")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'Already Available', but it was already here." in captured.out
    assert lm.inventory["ALREADY"].is_available is True


def test_show_inventory_empty(capsys):
    lm = LibraryManager()
    lm.show_inventory()
    captured = capsys.readouterr()
    assert "\n--- Current Library Inventory ---" in captured.out
    assert "The library is empty." in captured.out
    assert "---------------------------------" in captured.out


def test_show_inventory_non_empty(capsys):
    lm = LibraryManager()
    lm.add_book("Book One", "Author One", "ISBN1")
    lm.add_book("Book Two", "Author Two", "ISBN2")
    lm.borrow_book("ISBN2")  # Borrow second book
    lm.show_inventory()
    captured = capsys.readouterr()
    # Header and footer
    assert "\n--- Current Library Inventory ---" in captured.out
    assert "---------------------------------" in captured.out
    # Check that both books appear with correct status
    assert "[Available] Book One by Author One (ISBN: ISBN1)" in captured.out
    assert "[Borrowed] Book Two by Author Two (ISBN: ISBN2)" in captured.out
    # Ensure the order is not guaranteed but both are present
    assert captured.out.count("[") == 2


def test_add_book_with_exact_minimum_isbn_length(capsys):
    lm = LibraryManager()
    lm.add_book("Exact ISBN", "Author", "123")
    captured = capsys.readouterr()
    assert "Success: Added 'Exact ISBN' to the library." in captured.out
    assert "123" in lm.inventory


def test_add_book_with_long_isbn(capsys):
    lm = LibraryManager()
    long_isbn = "ISBN" + "X" * 50
    lm.add_book("Long ISBN Book", "Author", long_isbn)
    captured = capsys.readouterr()
    assert f"Success: Added 'Long ISBN Book' to the library." in captured.out
    assert long_isbn in lm.inventory


def test_inventory_contains_only_book_objects():
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "TESTISBN")
    assert isinstance(lm.inventory["TESTISBN"], Book)
    assert lm.inventory["TESTISBN"].title == "Test Book"
    assert lm.inventory["TESTISBN"].author == "Test Author"
    assert lm.inventory["TESTISBN"].isbn == "TESTISBN"


def test_borrow_and_return_toggle_is_available():
    lm = LibraryManager()
    lm.add_book("Toggle Book", "Author", "TOGGLE")
    # Initially available
    assert lm.inventory["TOGGLE"].is_available is True
    lm.borrow_book("TOGGLE")
    assert lm.inventory["TOGGLE"].is_available is False
    lm.return_book("TOGGLE")
    assert lm.inventory["TOGGLE"].is_available is True




