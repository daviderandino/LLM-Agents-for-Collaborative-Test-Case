import pytest
from data.input_code.library import Book, LibraryManager


@pytest.fixture
def lib():
    """Return a fresh LibraryManager instance for each test."""
    return LibraryManager()


def test_book_initialization_and_str(lib):
    title = "1984"
    author = "George Orwell"
    isbn = "1234567890"
    book = Book(title, author, isbn)

    # Initialization
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn
    assert book.is_available is True

    # __str__ output
    expected_str = f"[Available] {title} by {author} (ISBN: {isbn})"
    assert str(book) == expected_str
    assert isinstance(str(book), str)
    assert title in str(book)
    assert author in str(book)
    assert isbn in str(book)
    assert "Available" in str(book)
    assert "Borrowed" not in str(book)


def test_book_str_status_change(lib):
    book = Book("Title", "Author", "ISBN")
    assert "[Available]" in str(book)
    book.is_available = False
    assert "[Borrowed]" in str(book)
    assert "Available" not in str(book)
    assert "Borrowed" in str(book)


def test_inventory_is_dict_and_types(lib):
    assert isinstance(lib.inventory, dict)
    lib.add_book("Book1", "Author1", "ISBN1")
    assert isinstance(lib.inventory, dict)
    assert all(isinstance(k, str) for k in lib.inventory.keys())
    assert all(isinstance(v, Book) for v in lib.inventory.values())


def test_add_book_success_and_return_value(lib, capsys):
    lib.add_book("Book1", "Author1", "ISBN1")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'Book1' to the library."
    assert lib.inventory["ISBN1"].title == "Book1"
    assert lib.inventory["ISBN1"].is_available is True
    assert lib.add_book("Book2", "Author2", "ISBN2") is None
    assert len(lib.inventory) == 2


def test_add_book_duplicate_and_short_isbn(lib, capsys):
    lib.add_book("Book1", "Author1", "ISBN1")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'Book1' to the library."

    # Duplicate ISBN
    lib.add_book("BookDuplicate", "AuthorDup", "ISBN1")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: A book with ISBN ISBN1 already exists."
    assert len(lib.inventory) == 1

    # Short ISBN
    lib.add_book("ShortISBN", "AuthorShort", "12")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: ISBN '12' is too short."
    assert len(lib.inventory) == 1


def test_add_book_edge_cases(lib, capsys):
    # ISBN exactly 3 characters
    lib.add_book("Edge3", "AuthorEdge", "123")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'Edge3' to the library."
    assert "123" in lib.inventory

    # ISBN with special characters
    lib.add_book("Special", "AuthorSpec", "12-34")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'Special' to the library."
    assert "12-34" in lib.inventory


def test_borrow_book_success_and_return_value(lib, capsys):
    lib.add_book("Borrowable", "AuthorB", "ISBNB")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'Borrowable' to the library."

    lib.borrow_book("ISBNB")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: You have borrowed 'Borrowable'."
    assert lib.inventory["ISBNB"].is_available is False
    assert lib.borrow_book("ISBNB") is None


def test_borrow_book_errors(lib, capsys):
    # Non-existent ISBN
    lib.borrow_book("NONEXIST")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: Book with ISBN NONEXIST not found."

    # Borrow already borrowed
    lib.add_book("BookA", "AuthorA", "ISBNA")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'BookA' to the library."
    lib.borrow_book("ISBNA")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: You have borrowed 'BookA'."
    lib.borrow_book("ISBNA")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Unavailable: 'BookA' is currently borrowed by someone else."
    assert lib.inventory["ISBNA"].is_available is False


def test_return_book_success_and_return_value(lib, capsys):
    lib.add_book("Returnable", "AuthorR", "ISBNR")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'Returnable' to the library."

    lib.borrow_book("ISBNR")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: You have borrowed 'Returnable'."

    lib.return_book("ISBNR")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: 'Returnable' has been returned."
    assert lib.inventory["ISBNR"].is_available is True
    assert lib.return_book("ISBNR") is None


def test_return_book_errors(lib, capsys):
    # Non-existent ISBN
    lib.return_book("NONEXIST")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: We do not own a book with ISBN NONEXIST."

    # Return already available
    lib.add_book("BookC", "AuthorC", "ISBNC")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'BookC' to the library."
    lib.return_book("ISBNC")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Strange: You are trying to return 'BookC', but it was already here."
    assert lib.inventory["ISBNC"].is_available is True

    # Return borrowed book
    lib.borrow_book("ISBNC")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: You have borrowed 'BookC'."
    lib.return_book("ISBNC")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: 'BookC' has been returned."
    assert lib.inventory["ISBNC"].is_available is True


def test_show_inventory_empty(lib, capsys):
    lib.show_inventory()
    captured = capsys.readouterr()
    expected_header = "\n--- Current Library Inventory ---"
    expected_footer = "---------------------------------\n\n"
    assert captured.out.startswith(expected_header)
    assert "The library is empty." in captured.out
    assert captured.out.endswith(expected_footer)


def test_show_inventory_non_empty(lib, capsys):
    lib.add_book("Book1", "Author1", "ISBN1")
    lib.add_book("Book2", "Author2", "ISBN2")
    captured = capsys.readouterr()
    # Capture inventory after adding books
    lib.show_inventory()
    captured = capsys.readouterr()
    expected_header = "\n--- Current Library Inventory ---"
    expected_footer = "---------------------------------\n\n"
    assert captured.out.startswith(expected_header)
    assert captured.out.endswith(expected_footer)
    # Extract lines between header and footer
    body = captured.out[len(expected_header):-len(expected_footer)].strip().splitlines()
    # There should be two lines, one for each book
    assert len(body) == 2
    # Verify that each line matches the __str__ of the corresponding book
    book1_str = str(lib.inventory["ISBN1"])
    book2_str = str(lib.inventory["ISBN2"])
    assert book1_str in body
    assert book2_str in body


def test_show_inventory_returns_none(lib):
    assert lib.show_inventory() is None


def test_show_inventory_borrowed_status(lib, capsys):
    lib.add_book("AvailableBook", "AuthorA", "ISBN_A")
    lib.add_book("BorrowedBook", "AuthorB", "ISBN_B")
    lib.borrow_book("ISBN_B")
    lib.show_inventory()
    captured = capsys.readouterr()
    body = captured.out.splitlines()
    # Find the lines that contain the books
    available_line = next(line for line in body if "ISBN_A" in line)
    borrowed_line = next(line for line in body if "ISBN_B" in line)
    assert "[Available]" in available_line
    assert "[Borrowed]" in borrowed_line


def test_show_inventory_no_side_effects(lib, capsys):
    lib.add_book("BookX", "AuthorX", "ISBNX")
    original_inventory = lib.inventory.copy()
    lib.show_inventory()
    captured = capsys.readouterr()
    assert lib.inventory == original_inventory


def test_show_inventory_order(lib, capsys):
    lib.add_book("First", "Author1", "ISBN1")
    lib.add_book("Second", "Author2", "ISBN2")
    lib.add_book("Third", "Author3", "ISBN3")
    lib.show_inventory()
    captured = capsys.readouterr()
    body = captured.out.splitlines()
    # Extract only the book lines
    book_lines = [line for line in body if "ISBN" in line]
    expected_order = [
        str(lib.inventory["ISBN1"]),
        str(lib.inventory["ISBN2"]),
        str(lib.inventory["ISBN3"]),
    ]
    assert book_lines == expected_order


def test_show_inventory_footer_newline(lib, capsys):
    lib.add_book("BookY", "AuthorY", "ISBNY")
    lib.show_inventory()
    captured = capsys.readouterr()
    # Footer should end with two newlines
    assert captured.out.endswith("---------------------------------\n\n")


def test_show_inventory_header_newline(lib, capsys):
    lib.show_inventory()
    captured = capsys.readouterr()
    assert captured.out.startswith("\n--- Current Library Inventory ---")


def test_add_book_returns_none(lib):
    result = lib.add_book("TestBook", "TestAuthor", "ISBN123")
    assert result is None


def test_borrow_book_returns_none(lib):
    lib.add_book("TestBook", "TestAuthor", "ISBN123")
    result = lib.borrow_book("ISBN123")
    assert result is None


def test_return_book_returns_none(lib):
    lib.add_book("TestBook", "TestAuthor", "ISBN123")
    lib.borrow_book("ISBN123")
    result = lib.return_book("ISBN123")
    assert result is None


def test_state_consistency(lib, capsys):
    # Add a book
    lib.add_book("StateBook", "StateAuthor", "ISBNState")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'StateBook' to the library."
    assert lib.inventory["ISBNState"].is_available is True

    # Borrow the book
    lib.borrow_book("ISBNState")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: You have borrowed 'StateBook'."
    assert lib.inventory["ISBNState"].is_available is False

    # Return the book
    lib.return_book("ISBNState")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: 'StateBook' has been returned."
    assert lib.inventory["ISBNState"].is_available is True

    # Attempt invalid operations and ensure state unchanged
    lib.borrow_book("NONEXIST")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: Book with ISBN NONEXIST not found."
    assert len(lib.inventory) == 1

    lib.return_book("NONEXIST")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: We do not own a book with ISBN NONEXIST."
    assert len(lib.inventory) == 1

    lib.add_book("StateBook", "StateAuthor", "ISBNState")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: A book with ISBN ISBNState already exists."
    assert len(lib.inventory) == 1

    lib.add_book("Short", "Author", "12")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: ISBN '12' is too short."
    assert len(lib.inventory) == 1