import pytest
from data.input_code.d07_library import Book, LibraryManager

def test_book_init():
    book = Book("Test Book", "Test Author", "1234567890")
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.isbn == "1234567890"
    assert book.is_available

def test_book_str_available():
    book = Book("Test Book", "Test Author", "1234567890")
    assert str(book) == "[Available] Test Book by Test Author (ISBN: 1234567890)"

def test_book_str_borrowed():
    book = Book("Test Book", "Test Author", "1234567890")
    book.is_available = False
    assert str(book) == "[Borrowed] Test Book by Test Author (ISBN: 1234567890)"

@pytest.mark.parametrize("title,author,isbn,expected_output", [
    ("Test Book", "Test Author", "1234567890", "Success: Added 'Test Book' to the library.\n"),
])
def test_library_init_add_book(title, author, isbn, expected_output, capsys):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out == expected_output

def test_add_book_short_isbn(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "12")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: ISBN '12' is too short.\n"

def test_add_book_duplicate(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.add_book("Test Book", "Test Author", "1234567890")
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Test Book' to the library.\n[!] Error: A book with ISBN 1234567890 already exists.\n"

@pytest.mark.parametrize("isbn", [
    "1234567890",
])
def test_borrow_book_ok(isbn, capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", isbn)
    library.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out == f"Success: Added 'Test Book' to the library.\nSuccess: You have borrowed 'Test Book'.\n"

def test_borrow_book_unavailable(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.borrow_book("1234567890")
    library.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Test Book' to the library.\nSuccess: You have borrowed 'Test Book'.\n[!] Unavailable: 'Test Book' is currently borrowed by someone else.\n"

def test_borrow_book_not_found(capsys):
    library = LibraryManager()
    library.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: Book with ISBN 1234567890 not found.\n"

@pytest.mark.parametrize("isbn", [
    "1234567890",
])
def test_return_book_ok(isbn, capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", isbn)
    library.borrow_book(isbn)
    library.return_book(isbn)
    captured = capsys.readouterr()
    assert captured.out == f"Success: Added 'Test Book' to the library.\nSuccess: You have borrowed 'Test Book'.\nSuccess: 'Test Book' has been returned.\n"

def test_return_book_already_returned(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.return_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Test Book' to the library.\n[!] Strange: You are trying to return 'Test Book', but it was already here.\n"

def test_return_book_not_found(capsys):
    library = LibraryManager()
    library.return_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: We do not own a book with ISBN 1234567890.\n"

def test_show_inventory_empty(capsys):
    library = LibraryManager()
    library.show_inventory()
    captured = capsys.readouterr()
    assert captured.out == "\n--- Current Library Inventory ---\nThe library is empty.\n---------------------------------\n\n"

@pytest.mark.parametrize("title,author,isbn", [
    ("Test Book", "Test Author", "1234567890"),
])
def test_show_inventory_non_empty(title, author, isbn, capsys):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    library.show_inventory()
    captured = capsys.readouterr()
    expected = f"Success: Added '{title}' to the library.\n\n--- Current Library Inventory ---\n[Available] {title} by {author} (ISBN: {isbn})\n---------------------------------\n\n"
    assert captured.out == expected