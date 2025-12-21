import pytest
from data.input_code.library import Book, LibraryManager


@pytest.fixture
def lib():
    """Return a fresh LibraryManager instance."""
    return LibraryManager()


def test_book_initialization_and_str():
    """Test that a Book is initialized correctly and its string representation."""
    book = Book("1984", "George Orwell", "1234567890")
    assert book.title == "1984"
    assert book.author == "George Orwell"
    assert book.isbn == "1234567890"
    assert book.is_available is True

    expected_str = "[Available] 1984 by George Orwell (ISBN: 1234567890)"
    assert str(book) == expected_str

    # Borrow the book and check string changes
    book.is_available = False
    expected_str_borrowed = "[Borrowed] 1984 by George Orwell (ISBN: 1234567890)"
    assert str(book) == expected_str_borrowed


def test_library_manager_initialization(lib):
    """Test that a new LibraryManager starts with an empty inventory."""
    assert isinstance(lib.inventory, dict)
    assert lib.inventory == {}


@pytest.mark.parametrize(
    "title,author,isbn,expected_msg,expected_status",
    [
        ("The Hobbit", "J.R.R. Tolkien", "111", "Success: Added 'The Hobbit' to the library.", True),
        ("", "Anonymous", "222", "Success: Added '' to the library.", True),
        ("Mystery", "", "333", "Success: Added 'Mystery' to the library.", True),
        ("", "", "444", "Success: Added '' to the library.", True),
    ],
)
def test_add_book_success(lib, title, author, isbn, expected_msg, expected_status, capsys):
    """Test adding books with valid ISBNs and various title/author combinations."""
    lib.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_msg

    # Inventory should contain the new book
    assert isbn in lib.inventory
    book = lib.inventory[isbn]
    assert isinstance(book, Book)
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn
    assert book.is_available == expected_status


def test_add_book_errors(lib, capsys):
    """Test error conditions when adding books."""
    # ISBN too short
    lib.add_book("Short ISBN", "Author", "12")
    out, _ = capsys.readouterr()
    assert out.strip() == "[!] Error: ISBN '12' is too short."
    assert lib.inventory == {}

    # Duplicate ISBN
    lib.add_book("First Book", "Author", "555")
    out, _ = capsys.readouterr()
    assert out.strip() == "Success: Added 'First Book' to the library."
    lib.add_book("Duplicate Book", "Author", "555")
    out, _ = capsys.readouterr()
    assert out.strip() == "[!] Error: A book with ISBN 555 already exists."
    # Inventory should still contain only the first book
    assert len(lib.inventory) == 1
    assert lib.inventory["555"].title == "First Book"


def test_borrow_book(lib, capsys):
    """Test borrowing books under various conditions."""
    # Borrow non-existent book
    lib.borrow_book("999")
    out, _ = capsys.readouterr()
    assert out.strip() == "[!] Error: Book with ISBN 999 not found."

    # Add a book and borrow it
    lib.add_book("Brave New World", "Aldous Huxley", "777")
    out, _ = capsys.readouterr()
    assert out.strip() == "Success: Added 'Brave New World' to the library."

    lib.borrow_book("777")
    out, _ = capsys.readouterr()
    assert out.strip() == "Success: You have borrowed 'Brave New World'."
    assert lib.inventory["777"].is_available is False

    # Borrow the same book again
    lib.borrow_book("777")
    out, _ = capsys.readouterr()
    assert out.strip() == "[!] Unavailable: 'Brave New World' is currently borrowed by someone else."


def test_return_book(lib, capsys):
    """Test returning books under various conditions."""
    # Return non-existent book
    lib.return_book("888")
    out, _ = capsys.readouterr()
    assert out.strip() == "[!] Error: We do not own a book with ISBN 888."

    # Add a book, borrow it, then return it
    lib.add_book("Fahrenheit 451", "Ray Bradbury", "666")
    out, _ = capsys.readouterr()
    assert out.strip() == "Success: Added 'Fahrenheit 451' to the library."

    lib.borrow_book("666")
    out, _ = capsys.readouterr()
    assert out.strip() == "Success: You have borrowed 'Fahrenheit 451'."

    lib.return_book("666")
    out, _ = capsys.readouterr()
    assert out.strip() == "Success: 'Fahrenheit 451' has been returned."
    assert lib.inventory["666"].is_available is True

    # Return the same book again
    lib.return_book("666")
    out, _ = capsys.readouterr()
    assert out.strip() == "[!] Strange: You are trying to return 'Fahrenheit 451', but it was already here."


def test_show_inventory_empty(lib, capsys):
    """Test that show_inventory prints the correct message when inventory is empty."""
    lib.show_inventory()
    out, _ = capsys.readouterr()
    lines = out.splitlines()
    assert lines[0] == ""  # leading newline
    assert lines[1] == "--- Current Library Inventory ---"
    assert lines[2] == "The library is empty."
    assert lines[3] == "---------------------------------"


def test_show_inventory_multiple(lib, capsys):
    """Test that show_inventory prints all books in insertion order."""
    books = [
        ("Book A", "Author A", "A11"),
        ("Book B", "Author B", "B22"),
        ("Book C", "Author C", "C33"),
    ]
    for title, author, isbn in books:
        lib.add_book(title, author, isbn)
        capsys.readouterr()  # clear output

    lib.show_inventory()
    out, _ = capsys.readouterr()
    lines = out.splitlines()

    # Header and footer
    assert lines[0] == ""
    assert lines[1] == "--- Current Library Inventory ---"
    assert lines[-2] == "---------------------------------"

    # There should be one line per book between header and footer
    book_lines = lines[2:-2]  # exclude footer and trailing empty line
    assert len(book_lines) == len(books)

    # Verify each book line matches the __str__ representation
    for (title, author, isbn), line in zip(books, book_lines):
        expected = f"[Available] {title} by {author} (ISBN: {isbn})"
        assert line == expected

    # Borrow one book and check status update in inventory display
    lib.borrow_book("B22")
    capsys.readouterr()
    lib.show_inventory()
    out, _ = capsys.readouterr()
    lines = out.splitlines()
    book_lines = lines[2:-2]
    # Find the borrowed book line
    borrowed_line = next(l for l in book_lines if "Book B" in l)
    assert borrowed_line == "[Borrowed] Book B by Author B (ISBN: B22)"


def test_error_and_success_message_prefixes(lib, capsys):
    """Ensure that error messages start with '[!]' and success messages start with 'Success:'."""
    # Add book with short ISBN
    lib.add_book("Error Book", "Author", "1")
    out, _ = capsys.readouterr()
    assert out.strip().startswith("[!]")

    # Add valid book
    lib.add_book("Success Book", "Author", "123")
    out, _ = capsys.readouterr()
    assert out.strip().startswith("Success:")

    # Borrow non-existent
    lib.borrow_book("999")
    out, _ = capsys.readouterr()
    assert out.strip().startswith("[!]")

    # Borrow valid
    lib.borrow_book("123")
    out, _ = capsys.readouterr()
    assert out.strip().startswith("Success:")

    # Return non-existent
    lib.return_book("999")
    out, _ = capsys.readouterr()
    assert out.strip().startswith("[!]")

    # Return valid
    lib.return_book("123")
    out, _ = capsys.readouterr()
    assert out.strip().startswith("Success:")


def test_inventory_contents_and_types(lib):
    """Verify that inventory keys are ISBN strings and values are Book instances."""
    lib.add_book("Alpha", "A", "X12")
    lib.add_book("Beta", "B", "X23")
    assert set(lib.inventory.keys()) == {"X12", "X23"}
    for book in lib.inventory.values():
        assert isinstance(book, Book)


def test_add_book_with_empty_isbn(lib, capsys):
    """Adding a book with an empty ISBN should trigger an error."""
    lib.add_book("Empty ISBN", "Author", "")
    out, _ = capsys.readouterr()
    assert out.strip() == "[!] Error: ISBN '' is too short."
    assert lib.inventory == {}


def test_borrow_and_return_with_empty_isbn(lib, capsys):
    """Borrowing or returning with an empty ISBN should trigger an error."""
    lib.borrow_book("")
    out, _ = capsys.readouterr()
    assert out.strip() == "[!] Error: Book with ISBN  not found."

    lib.return_book("")
    out, _ = capsys.readouterr()
    assert out.strip() == "[!] Error: We do not own a book with ISBN ."


def test_show_inventory_after_borrow_and_return(lib, capsys):
    """Show inventory reflects status changes after borrow and return."""
    lib.add_book("Test Book", "Tester", "T123")
    capsys.readouterr()
    lib.borrow_book("T123")
    capsys.readouterr()
    lib.show_inventory()
    out, _ = capsys.readouterr()
    lines = out.splitlines()
    # Find the book line
    book_line = next(l for l in lines if "Test Book" in l)
    assert book_line == "[Borrowed] Test Book by Tester (ISBN: T123)"

    lib.return_book("T123")
    capsys.readouterr()
    lib.show_inventory()
    out, _ = capsys.readouterr()
    lines = out.splitlines()
    book_line = next(l for l in lines if "Test Book" in l)
    assert book_line == "[Available] Test Book by Tester (ISBN: T123)"


def test_add_book_with_long_title_and_author(lib, capsys):
    """Adding a book with very long title and author should succeed."""
    long_title = "A" * 1000
    long_author = "B" * 1000
    isbn = "LONGISBN123"
    lib.add_book(long_title, long_author, isbn)
    out, _ = capsys.readouterr()
    assert out.strip() == f"Success: Added '{long_title}' to the library."
    assert isbn in lib.inventory
    book = lib.inventory[isbn]
    assert book.title == long_title
    assert book.author == long_author
    assert book.isbn == isbn
    # Check string representation length
    assert len(str(book)) > 2000


def test_add_book_with_long_isbn(lib, capsys):
    """Adding a book with a very long ISBN should succeed."""
    long_isbn = "I" * 1000
    lib.add_book("Long ISBN Book", "Author", long_isbn)
    out, _ = capsys.readouterr()
    assert out.strip() == f"Success: Added 'Long ISBN Book' to the library."
    assert long_isbn in lib.inventory
    book = lib.inventory[long_isbn]
    assert book.isbn == long_isbn


def test_add_book_with_special_characters(lib, capsys):
    """Adding a book with special characters in title, author, and ISBN."""
    title = "Café ☕️"
    author = "Jürgen Müller"
    isbn = "ISBN-特殊字符"
    lib.add_book(title, author, isbn)
    out, _ = capsys.readouterr()
    assert out.strip() == f"Success: Added '{title}' to the library."
    assert isbn in lib.inventory
    book = lib.inventory[isbn]
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn
    assert str(book) == f"[Available] {title} by {author} (ISBN: {isbn})"


def test_borrow_and_return_with_long_isbn(lib, capsys):
    """Borrowing and returning a book with a very long ISBN."""
    long_isbn = "L" * 500
    lib.add_book("Long ISBN Book", "Author", long_isbn)
    capsys.readouterr()
    lib.borrow_book(long_isbn)
    out, _ = capsys.readouterr()
    assert out.strip() == f"Success: You have borrowed 'Long ISBN Book'."
    assert lib.inventory[long_isbn].is_available is False

    lib.return_book(long_isbn)
    out, _ = capsys.readouterr()
    assert out.strip() == f"Success: 'Long ISBN Book' has been returned."
    assert lib.inventory[long_isbn].is_available is True


def test_show_inventory_multiple_borrow_return(lib, capsys):
    """Show inventory after multiple borrow and return operations."""
    books = [
        ("Book One", "Author One", "ONE1"),
        ("Book Two", "Author Two", "TWO2"),
        ("Book Three", "Author Three", "THREE3"),
    ]
    for title, author, isbn in books:
        lib.add_book(title, author, isbn)
        capsys.readouterr()

    # Borrow first and third
    lib.borrow_book("ONE1")
    lib.borrow_book("THREE3")
    capsys.readouterr()

    # Return second (which was never borrowed)
    lib.return_book("TWO2")
    capsys.readouterr()

    lib.show_inventory()
    out, _ = capsys.readouterr()
    lines = out.splitlines()
    book_lines = lines[2:-2]
    expected_status = {
        "ONE1": "[Borrowed] Book One by Author One (ISBN: ONE1)",
        "TWO2": "[Available] Book Two by Author Two (ISBN: TWO2)",
        "THREE3": "[Borrowed] Book Three by Author Three (ISBN: THREE3)",
    }
    for line in book_lines:
        for isbn, expected in expected_status.items():
            if f"ISBN: {isbn}" in line:
                assert line == expected


def test_show_inventory_with_whitespace_titles_and_authors(lib, capsys):
    """Adding books with whitespace in title and author."""
    lib.add_book("   Leading and trailing spaces   ", "   Author Name   ", "WS1")
    capsys.readouterr()
    lib.show_inventory()
    out, _ = capsys.readouterr()
    lines = out.splitlines()
    book_line = next(l for l in lines if "WS1" in l)
    assert book_line == "[Available]    Leading and trailing spaces    by     Author Name    (ISBN: WS1)"


def test_show_inventory_with_numeric_isbn(lib, capsys):
    """Adding books with numeric ISBNs."""
    lib.add_book("Numeric ISBN", "Numeric Author", "123456")
    capsys.readouterr()
    lib.show_inventory()
    out, _ = capsys.readouterr()
    lines = out.splitlines()
    book_line = next(l for l in lines if "123456" in l)
    assert book_line == "[Available] Numeric ISBN by Numeric Author (ISBN: 123456)"


def test_show_inventory_with_special_isbn(lib, capsys):
    """Adding books with special characters in ISBN."""
    lib.add_book("Special ISBN", "Special Author", "ISBN-!@#$%^&*()")
    capsys.readouterr()
    lib.show_inventory()
    out, _ = capsys.readouterr()
    lines = out.splitlines()
    book_line = next(l for l in lines if "ISBN-!@#$%^&*()" in l)
    assert book_line == "[Available] Special ISBN by Special Author (ISBN: ISBN-!@#$%^&*())"


def test_show_inventory_header_footer(lib, capsys):
    """Ensure header and footer are printed correctly."""
    lib.add_book("Header Test", "Header Author", "HT1")
    capsys.readouterr()
    lib.show_inventory()
    out, _ = capsys.readouterr()
    lines = out.splitlines()
    assert lines[1] == "--- Current Library Inventory ---"
    assert lines[-2] == "---------------------------------"


def test_show_inventory_line_count(lib, capsys):
    """Check that the number of lines corresponds to books + header/footer."""
    books = [("B1", "A1", "I1"), ("B2", "A2", "I2")]
    for title, author, isbn in books:
        lib.add_book(title, author, isbn)
        capsys.readouterr()
    lib.show_inventory()
    out, _ = capsys.readouterr()
    lines = out.splitlines()
    # 1 leading empty line, 1 header, 2 book lines, 1 footer
    assert len(lines) == 5


def test_book_str_special_characters():
    """Book __str__ should handle special characters correctly."""
    book = Book("Café", "Jürgen", "ISBN-123")
    expected = "[Available] Café by Jürgen (ISBN: ISBN-123)"
    assert str(book) == expected


def test_borrow_book_success_message(lib, capsys):
    """Borrowing a book should print a success message."""
    lib.add_book("Borrow Test", "Author", "BT1")
    capsys.readouterr()
    lib.borrow_book("BT1")
    out, _ = capsys.readouterr()
    assert out.strip() == "Success: You have borrowed 'Borrow Test'."


def test_return_book_success_message(lib, capsys):
    """Returning a book should print a success message."""
    lib.add_book("Return Test", "Author", "RT1")
    capsys.readouterr()
    lib.borrow_book("RT1")
    capsys.readouterr()
    lib.return_book("RT1")
    out, _ = capsys.readouterr()
    assert out.strip() == "Success: 'Return Test' has been returned."


def test_inventory_keys_are_strings(lib):
    """Inventory keys should be strings."""
    lib.add_book("String Key", "Author", "SK1")
    assert isinstance(list(lib.inventory.keys())[0], str)


def test_inventory_values_are_book_instances(lib):
    """Inventory values should be Book instances."""
    lib.add_book("Book Value", "Author", "BV1")
    assert isinstance(list(lib.inventory.values())[0], Book)