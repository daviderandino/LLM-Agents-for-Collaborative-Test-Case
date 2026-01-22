import pytest
from data.input_code.d07_library import Book, LibraryManager

def test_book_init():
    book = Book("Test Book", "Test Author", "1234567890")
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.isbn == "1234567890"
    assert book.is_available

def test_book_str():
    book = Book("Test Book", "Test Author", "1234567890")
    assert str(book) == "[Available] Test Book by Test Author (ISBN: 1234567890)"

def test_library_init():
    library = LibraryManager()
    assert library.inventory == {}

@pytest.mark.parametrize("title, author, isbn, expected", [
    ("Test Book2", "Test Author", "1234567891", "Success: Added 'Test Book2' to the library."),
    ("Test Book", "Test Author", "12", "[!] Error: ISBN '12' is too short."),
])
def test_add_book(capsys, title, author, isbn, expected):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected

def test_add_duplicate_book(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.add_book("Test Book", "Test Author", "1234567890")
    captured = capsys.readouterr()
    out = captured.out.strip().splitlines()
    assert out[0] == "Success: Added 'Test Book' to the library."
    assert out[1] == "[!] Error: A book with ISBN 1234567890 already exists."

@pytest.mark.parametrize("isbn, expected", [
    ("1234567890", "Success: You have borrowed 'Test Book'."),
    ("9876543210", "[!] Error: Book with ISBN 9876543210 not found."),
])
def test_borrow_book(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.borrow_book(isbn)
    captured = capsys.readouterr()
    out = captured.out.strip().splitlines()
    if len(out) > 1:
        assert out[0] == "Success: Added 'Test Book' to the library."
        assert out[1] == expected
    else:
        assert out[0] == expected

def test_borrow_unavailable_book(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.borrow_book("1234567890")
    library.borrow_book("1234567890")
    captured = capsys.readouterr()
    out = captured.out.strip().splitlines()
    assert out[0] == "Success: Added 'Test Book' to the library."
    assert out[1] == "Success: You have borrowed 'Test Book'."
    assert out[2] == "[!] Unavailable: 'Test Book' is currently borrowed by someone else."

@pytest.mark.parametrize("isbn, expected", [
    ("1234567890", "Success: 'Test Book' has been returned."),
    ("9876543210", "[!] Error: We do not own a book with ISBN 9876543210."),
])
def test_return_book(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.borrow_book("1234567890")
    library.return_book(isbn)
    captured = capsys.readouterr()
    out = captured.out.strip().splitlines()
    assert out[0] == "Success: Added 'Test Book' to the library."
    assert out[1] == "Success: You have borrowed 'Test Book'."
    if out[-1] == expected:
        pass
    else:
        assert out[-1] == expected

def test_return_already_returned_book(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.borrow_book("1234567890")
    library.return_book("1234567890")
    library.return_book("1234567890")
    captured = capsys.readouterr()
    out = captured.out.strip().splitlines()
    assert out[0] == "Success: Added 'Test Book' to the library."
    assert out[1] == "Success: You have borrowed 'Test Book'."
    assert out[2] == "Success: 'Test Book' has been returned."
    assert out[3] == "[!] Strange: You are trying to return 'Test Book', but it was already here."

def test_show_inventory_empty(capsys):
    library = LibraryManager()
    library.show_inventory()
    captured = capsys.readouterr()
    out = captured.out.strip().splitlines()
    assert out == ["--- Current Library Inventory ---", "The library is empty.", "---------------------------------"]

def test_show_inventory(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.show_inventory()
    captured = capsys.readouterr()
    out = captured.out.strip().splitlines()
    assert out[0] == "Success: Added 'Test Book' to the library."
    assert library.inventory
    library.show_inventory()
    captured = capsys.readouterr()
    out = captured.out.strip().splitlines()
    assert out[0] == "--- Current Library Inventory ---"
    assert out[1] == "[Available] Test Book by Test Author (ISBN: 1234567890)"
    assert out[2] == "---------------------------------"