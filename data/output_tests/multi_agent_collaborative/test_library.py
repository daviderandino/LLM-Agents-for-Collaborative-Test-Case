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
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", isbn)
    captured = capsys.readouterr() # Clear the output buffer
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
    captured = capsys.readouterr() # Clear the output buffer
    library.borrow_book("9780743273565")
    captured = capsys.readouterr()
    assert f"[!] Unavailable: 'The Great Gatsby' is currently borrowed by someone else." in captured.out

@pytest.mark.parametrize('isbn, expected', [
    ("9780743273565", None),
])
def test_library_manager_return_book(isbn, expected, capsys):
    library = LibraryManager()
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", isbn)
    library.borrow_book(isbn)
    captured = capsys.readouterr() # Clear the output buffer
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
    captured = capsys.readouterr() # Clear the output buffer
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
    captured = capsys.readouterr() # Clear the output buffer
    library.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] The Great Gatsby by F. Scott Fitzgerald (ISBN: 9780743273565)" in captured.out

@pytest.mark.parametrize('title, author, isbn', [
    ("Test", "Test", "12"),
])
def test_library_manager_add_book_isbn_length_3(title, author, isbn, capsys):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert f"[!] Error: ISBN '{isbn}' is too short." in captured.out

@pytest.mark.parametrize('title, author, isbn', [
    ("", "Test", "1234567890"),
])
def test_library_manager_add_book_empty_title(title, author, isbn, capsys):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert f"Success: Added '{title}' to the library." in captured.out

@pytest.mark.parametrize('title, author, isbn', [
    ("Test", "", "1234567890"),
])
def test_library_manager_add_book_empty_author(title, author, isbn, capsys):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert f"Success: Added '{title}' to the library." in captured.out

def test_library_manager_return_book_not_borrowed(capsys):
    library = LibraryManager()
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
    captured = capsys.readouterr() # Clear the output buffer
    library.return_book("9780743273565")
    captured = capsys.readouterr()
    assert f"[!] Strange: You are trying to return 'The Great Gatsby', but it was already here." in captured.out

def test_library_manager_borrow_book_available_after_return(capsys):
    library = LibraryManager()
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
    library.borrow_book("9780743273565")
    captured = capsys.readouterr() # Clear the output buffer
    library.return_book("9780743273565")
    captured = capsys.readouterr() # Clear the output buffer
    library.borrow_book("9780743273565")
    captured = capsys.readouterr()
    assert f"Success: You have borrowed 'The Great Gatsby'." in captured.out