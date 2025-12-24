import pytest
from data.input_code.library import *

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("To Kill a Mockingbird", "Harper Lee", "9780061120084", None)
])
def test_book_init(title, author, isbn, expected):
    book = Book(title, author, isbn)
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn
    assert book.is_available == True

def test_book_str():
    book = Book("1984", "George Orwell", "9780451524935")
    assert str(book) == "[Available] 1984 by George Orwell (ISBN: 9780451524935)"

def test_library_manager_init():
    library = LibraryManager()
    assert library.inventory == {}

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", None),
    ("Pride and Prejudice", "Jane Austen", "123", None),
])
def test_library_manager_add_book(title, author, isbn, expected, capsys):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    if len(isbn) < 3:
        assert f"[!] Error: ISBN '{isbn}' is too short." in captured.out
    else:
        assert f"Success: Added '{title}' to the library." in captured.out

def test_library_manager_add_book_duplicate(capsys):
    library = LibraryManager()
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
    captured = capsys.readouterr()
    assert f"[!] Error: A book with ISBN 9780743273565 already exists." in captured.out

@pytest.mark.parametrize('isbn, expected', [
    ("9780743273565", None),
])
def test_library_manager_borrow_book(isbn, expected, capsys):
    library = LibraryManager()
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
    library.borrow_book(isbn)
    captured = capsys.readouterr()
    assert f"Success: You have borrowed 'The Great Gatsby'." in captured.out

def test_library_manager_borrow_book_not_found(capsys):
    library = LibraryManager()
    library.borrow_book("9780743273565")
    captured = capsys.readouterr()
    assert f"[!] Error: Book with ISBN 9780743273565 not found." in captured.out

def test_library_manager_borrow_book_unavailable(capsys):
    library = LibraryManager()
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
    library.borrow_book("9780743273565")
    library.borrow_book("9780743273565")
    captured = capsys.readouterr()
    assert f"[!] Unavailable: 'The Great Gatsby' is currently borrowed by someone else." in captured.out

@pytest.mark.parametrize('isbn, expected', [
    ("9780743273565", None),
])
def test_library_manager_return_book(isbn, expected, capsys):
    library = LibraryManager()
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
    library.borrow_book("9780743273565")
    library.return_book(isbn)
    captured = capsys.readouterr()
    assert f"Success: 'The Great Gatsby' has been returned." in captured.out

def test_library_manager_return_book_not_found(capsys):
    library = LibraryManager()
    library.return_book("9780743273565")
    captured = capsys.readouterr()
    assert f"[!] Error: We do not own a book with ISBN 9780743273565." in captured.out

def test_library_manager_return_book_already_available(capsys):
    library = LibraryManager()
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
    library.return_book("9780743273565")
    captured = capsys.readouterr()
    assert f"[!] Strange: You are trying to return 'The Great Gatsby', but it was already here." in captured.out

def test_library_manager_show_inventory_empty(capsys):
    library = LibraryManager()
    library.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_library_manager_show_inventory_not_empty(capsys):
    library = LibraryManager()
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
    library.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] The Great Gatsby by F. Scott Fitzgerald (ISBN: 9780743273565)" in captured.out

import pytest
from data.input_code.library import *

@pytest.mark.parametrize('title, author, isbn', [
    ("To Kill a Mockingbird", "Harper Lee", "9780061120084"),
])
def test_t1_init(title, author, isbn):
    book = Book(title, author, isbn)
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn
    assert book.is_available == True

def test_t2_str():
    book = Book("1984", "George Orwell", "9780451524935")
    assert str(book) == "[Available] 1984 by George Orwell (ISBN: 9780451524935)"

def test_t3_library_init():
    library = LibraryManager()
    assert library.inventory == {}

@pytest.mark.parametrize('title, author, isbn', [
    ("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565"),
])
def test_t4_add_book_ok(title, author, isbn, capsys):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert f"Success: Added '{title}' to the library." in captured.out

def test_t5_add_book_isbn_too_short(capsys):
    library = LibraryManager()
    library.add_book("Pride and Prejudice", "Jane Austen", "12")
    captured = capsys.readouterr()
    assert f"[!] Error: ISBN '12' is too short." in captured.out

def test_t6_add_book_duplicate(capsys):
    library = LibraryManager()
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
    captured = capsys.readouterr()
    assert f"[!] Error: A book with ISBN 9780743273565 already exists." in captured.out

@pytest.mark.parametrize('isbn', [
    ("9780743273565"),
])
def test_t7_borrow_book_ok(isbn, capsys):
    library = LibraryManager()
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
    library.borrow_book(isbn)
    captured = capsys.readouterr()
    assert f"Success: You have borrowed 'The Great Gatsby'." in captured.out

def test_t8_borrow_book_not_found(capsys):
    library = LibraryManager()
    library.borrow_book("9780743273565")
    captured = capsys.readouterr()
    assert f"[!] Error: Book with ISBN 9780743273565 not found." in captured.out

def test_t9_borrow_book_unavailable(capsys):
    library = LibraryManager()
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
    library.borrow_book("9780743273565")
    library.borrow_book("9780743273565")
    captured = capsys.readouterr()
    assert f"[!] Unavailable: 'The Great Gatsby' is currently borrowed by someone else." in captured.out

@pytest.mark.parametrize('isbn', [
    ("9780743273565"),
])
def test_t10_return_book_ok(isbn, capsys):
    library = LibraryManager()
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
    library.borrow_book("9780743273565")
    library.return_book(isbn)
    captured = capsys.readouterr()
    assert f"Success: 'The Great Gatsby' has been returned." in captured.out

def test_t11_return_book_not_found(capsys):
    library = LibraryManager()
    library.return_book("9780743273565")
    captured = capsys.readouterr()
    assert f"[!] Error: We do not own a book with ISBN 9780743273565." in captured.out

def test_t12_return_book_already_available(capsys):
    library = LibraryManager()
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
    library.return_book("9780743273565")
    captured = capsys.readouterr()
    assert f"[!] Strange: You are trying to return 'The Great Gatsby', but it was already here." in captured.out

def test_t13_show_inventory_empty(capsys):
    library = LibraryManager()
    library.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_t14_show_inventory_not_empty(capsys):
    library = LibraryManager()
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
    library.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] The Great Gatsby by F. Scott Fitzgerald (ISBN: 9780743273565)" in captured.out

def test_t_missing_isbn_length_3(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "12")
    captured = capsys.readouterr()
    assert f"[!] Error: ISBN '12' is too short." in captured.out

def test_t_missing_empty_title(capsys):
    library = LibraryManager()
    library.add_book("", "Test Author", "9780743273565")
    captured = capsys.readouterr()
    assert f"Success: Added '' to the library." in captured.out

def test_t_missing_empty_author(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "", "9780743273565")
    captured = capsys.readouterr()
    assert f"Success: Added 'Test Book' to the library." in captured.out

def test_t_missing_book_borderline_isbn(capsys):
    library = LibraryManager()
    library.borrow_book("9780743273565")
    captured = capsys.readouterr()
    assert f"[!] Error: Book with ISBN 9780743273565 not found." in captured.out

def test_t_missing_return_book_not_borrowed(capsys):
    library = LibraryManager()
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
    library.return_book("9780743273565")
    captured = capsys.readouterr()
    assert f"[!] Strange: You are trying to return 'The Great Gatsby', but it was already here." in captured.out