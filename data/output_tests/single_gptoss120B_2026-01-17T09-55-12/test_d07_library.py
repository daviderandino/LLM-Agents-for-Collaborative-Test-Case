from data.input_code.d07_library import Book, LibraryManager
import pytest

def test_book_str_representation():
    b = Book(title="1984", author="George Orwell", isbn="12345")
    assert str(b) == "[Available] 1984 by George Orwell (ISBN: 12345)"
    b.is_available = False
    assert str(b) == "[Borrowed] 1984 by George Orwell (ISBN: 12345)"

def test_add_book_success_and_inventory():
    lib = LibraryManager()
    lib.add_book("Dune", "Frank Herbert", "ISBN001")
    assert "ISBN001" in lib.inventory
    book = lib.inventory["ISBN001"]
    assert isinstance(book, Book)
    assert book.title == "Dune"
    assert book.is_available is True

def test_add_book_invalid_isbn_and_duplicate(capsys):
    lib = LibraryManager()
    # Invalid ISBN (too short)
    lib.add_book("Short ISBN", "Author", "12")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out
    assert "12" not in lib.inventory

    # Add a valid book then attempt duplicate
    lib.add_book("Valid Book", "Author", "ABC123")
    captured = capsys.readouterr()
    assert "Success: Added 'Valid Book' to the library." in captured.out
    lib.add_book("Another Title", "Other", "ABC123")
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN ABC123 already exists." in captured.out
    # Ensure original book unchanged
    assert lib.inventory["ABC123"].title == "Valid Book"

def test_borrow_and_return_flow(capsys):
    lib = LibraryManager()
    lib.add_book("The Hobbit", "J.R.R. Tolkien", "HOB123")
    capsys.readouterr()  # clear output

    # Borrow success
    lib.borrow_book("HOB123")
    out = capsys.readouterr().out
    assert "Success: You have borrowed 'The Hobbit'." in out
    assert lib.inventory["HOB123"].is_available is False

    # Borrow when already borrowed
    lib.borrow_book("HOB123")
    out = capsys.readouterr().out
    assert "[!] Unavailable: 'The Hobbit' is currently borrowed by someone else." in out
    assert lib.inventory["HOB123"].is_available is False

    # Return success
    lib.return_book("HOB123")
    out = capsys.readouterr().out
    assert "Success: 'The Hobbit' has been returned." in out
    assert lib.inventory["HOB123"].is_available is True

    # Return when already available
    lib.return_book("HOB123")
    out = capsys.readouterr().out
    assert "[!] Strange: You are trying to return 'The Hobbit', but it was already here." in out
    assert lib.inventory["HOB123"].is_available is True

def test_error_handling_for_nonexistent_isbn(capsys):
    lib = LibraryManager()
    # Borrow non‑existent
    lib.borrow_book("NOPE")
    out = capsys.readouterr().out
    assert "[!] Error: Book with ISBN NOPE not found." in out

    # Return non‑existent
    lib.return_book("NOPE")
    out = capsys.readouterr().out
    assert "[!] Error: We do not own a book with ISBN NOPE." in out

