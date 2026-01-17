import pytest
from data.input_code.d07_library import Book, LibraryManager


def test_book_str_available_and_borrowed():
    book = Book("1984", "George Orwell", "1234567890")
    # Default status should be available
    assert book.is_available is True
    expected_available = "[Available] 1984 by George Orwell (ISBN: 1234567890)"
    assert str(book) == expected_available

    # Change status to borrowed
    book.is_available = False
    expected_borrowed = "[Borrowed] 1984 by George Orwell (ISBN: 1234567890)"
    assert str(book) == expected_borrowed


def test_add_book_success_and_duplicate_and_short_isbn(capsys):
    manager = LibraryManager()

    # Successful addition
    manager.add_book("The Hobbit", "J.R.R. Tolkien", "978-0-123456-47-2")
    captured = capsys.readouterr()
    assert "Success: Added 'The Hobbit' to the library." in captured.out
    assert "978-0-123456-47-2" in manager.inventory
    assert isinstance(manager.inventory["978-0-123456-47-2"], Book)

    # Duplicate ISBN
    manager.add_book("Another Book", "Author", "978-0-123456-47-2")
    captured = capsys.readouterr()
    assert "Error: A book with ISBN 978-0-123456-47-2 already exists." in captured.out
    # Inventory should still contain only the first book
    assert len(manager.inventory) == 1

    # Short ISBN
    manager.add_book("Short ISBN", "Author", "12")
    captured = capsys.readouterr()
    assert "Error: ISBN '12' is too short." in captured.out
    # Inventory should remain unchanged
    assert len(manager.inventory) == 1


def test_borrow_book_success_and_errors(capsys):
    manager = LibraryManager()
    manager.add_book("Dune", "Frank Herbert", "978-0-123456-47-3")
    capsys.readouterr()  # clear output

    # Successful borrow
    manager.borrow_book("978-0-123456-47-3")
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'Dune'." in captured.out
    assert manager.inventory["978-0-123456-47-3"].is_available is False

    # Borrow again (already borrowed)
    manager.borrow_book("978-0-123456-47-3")
    captured = capsys.readouterr()
    assert "Unavailable: 'Dune' is currently borrowed by someone else." in captured.out

    # Borrow non-existent ISBN
    manager.borrow_book("000-0-000000-00-0")
    captured = capsys.readouterr()
    assert "Error: Book with ISBN 000-0-000000-00-0 not found." in captured.out


def test_return_book_success_and_errors(capsys):
    manager = LibraryManager()
    manager.add_book("Foundation", "Isaac Asimov", "978-0-123456-47-4")
    capsys.readouterr()  # clear output

    # Borrow first to set status to borrowed
    manager.borrow_book("978-0-123456-47-4")
    capsys.readouterr()

    # Successful return
    manager.return_book("978-0-123456-47-4")
    captured = capsys.readouterr()
    assert "Success: 'Foundation' has been returned." in captured.out
    assert manager.inventory["978-0-123456-47-4"].is_available is True

    # Return again (already available)
    manager.return_book("978-0-123456-47-4")
    captured = capsys.readouterr()
    assert "Strange: You are trying to return 'Foundation', but it was already here." in captured.out

    # Return non-existent ISBN
    manager.return_book("000-0-000000-00-0")
    captured = capsys.readouterr()
    assert "Error: We do not own a book with ISBN 000-0-000000-00-0." in captured.out


def test_show_inventory_empty_and_nonempty(capsys):
    manager = LibraryManager()

    # Empty inventory
    manager.show_inventory()
    captured = capsys.readouterr()
    assert "--- Current Library Inventory ---" in captured.out
    assert "The library is empty." in captured.out
    assert "---------------------------------" in captured.out

    # Add a book and show inventory
    manager.add_book("Brave New World", "Aldous Huxley", "978-0-123456-47-5")
    capsys.readouterr()  # clear output
    manager.show_inventory()
    captured = capsys.readouterr()
    assert "--- Current Library Inventory ---" in captured.out
    assert "[Available] Brave New World by Aldous Huxley (ISBN: 978-0-123456-47-5)" in captured.out
    assert "---------------------------------" in captured.out
    # Ensure the book string appears exactly once
    assert captured.out.count("Brave New World") == 1
    assert captured.out.count("[Available]") == 1
    assert captured.out.count("[Borrowed]") == 0
    assert "The library is empty." not in captured.out
    assert len(manager.inventory) == 1
    assert isinstance(manager.inventory["978-0-123456-47-5"], Book)
    assert manager.inventory["978-0-123456-47-5"].is_available is True