import pytest
from data.input_code.d07_library import *

def test_add_book_short_isbn(capsys):
    manager = LibraryManager()
    manager.add_book("Tiny Book", "A. Writer", "12")
    captured = capsys.readouterr().out
    assert captured == "[!] Error: ISBN '12' is too short.\n"

def test_add_book_success(capsys):
    manager = LibraryManager()
    manager.add_book("Good Book", "B. Author", "123")
    captured = capsys.readouterr().out
    assert captured == "Success: Added 'Good Book' to the library.\n"

def test_add_book_duplicate(capsys):
    manager = LibraryManager()
    manager.add_book("Good Book", "B. Author", "123")
    manager.add_book("Another Good Book", "C. Writer", "123")
    captured = capsys.readouterr().out
    # The duplicate error should be present in the output
    assert "[!] Error: A book with ISBN 123 already exists.\n" in captured

def test_borrow_book_not_exist(capsys):
    manager = LibraryManager()
    manager.borrow_book("999")
    captured = capsys.readouterr().out
    assert captured == "[!] Error: Book with ISBN 999 not found.\n"

def test_borrow_book_success(capsys):
    manager = LibraryManager()
    manager.add_book("Borrowable Book", "Author", "456")
    manager.borrow_book("456")
    captured = capsys.readouterr().out
    # The borrow success message should be present
    assert "Success: You have borrowed 'Borrowable Book'.\n" in captured

def test_borrow_book_unavailable(capsys):
    manager = LibraryManager()
    manager.add_book("Borrowable Book", "Author", "456")
    manager.borrow_book("456")
    manager.borrow_book("456")
    captured = capsys.readouterr().out
    # The unavailable message should be present
    assert "[!] Unavailable: 'Borrowable Book' is currently borrowed by someone else.\n" in captured

def test_return_book_not_exist(capsys):
    manager = LibraryManager()
    manager.return_book("000")
    captured = capsys.readouterr().out
    assert captured == "[!] Error: We do not own a book with ISBN 000.\n"

def test_return_book_already_available(capsys):
    manager = LibraryManager()
    manager.add_book("Lonely Book", "Author", "111")
    manager.return_book("111")
    captured = capsys.readouterr().out
    # The strange message should be present
    assert "[!] Strange: You are trying to return 'Lonely Book', but it was already here.\n" in captured

def test_return_book_success(capsys):
    manager = LibraryManager()
    manager.add_book("Borrowable Book", "Author", "456")
    manager.borrow_book("456")
    manager.return_book("456")
    captured = capsys.readouterr().out
    # The return success message should be present
    assert "Success: 'Borrowable Book' has been returned.\n" in captured

def test_show_inventory_empty(capsys):
    manager = LibraryManager()
    manager.show_inventory()
    captured = capsys.readouterr().out
    assert "The library is empty." in captured
    assert "--- Current Library Inventory ---" in captured
    assert "---------------------------------" in captured

def test_show_inventory_non_empty(capsys):
    manager = LibraryManager()
    manager.add_book("Available Book", "Author A", "123")
    manager.add_book("Borrowed Book", "Author B", "456")
    manager.borrow_book("456")
    manager.show_inventory()
    captured = capsys.readouterr().out
    assert "[Available] Available Book by Author A (ISBN: 123)" in captured
    assert "[Borrowed] Borrowed Book by Author B (ISBN: 456)" in captured
    assert "--- Current Library Inventory ---" in captured
    assert "---------------------------------" in captured

def test_book_str_available():
    book = Book("Free Book", "D. Writer", "777")
    book.is_available = True
    assert str(book) == "[Available] Free Book by D. Writer (ISBN: 777)"

def test_book_str_borrowed():
    book = Book("Taken Book", "E. Author", "888")
    book.is_available = False
    assert str(book) == "[Borrowed] Taken Book by E. Author (ISBN: 888)"