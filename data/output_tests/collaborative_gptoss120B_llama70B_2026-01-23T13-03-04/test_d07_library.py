import pytest
from data.input_code.d07_library import *

@pytest.mark.parametrize('title, author, isbn, expected', [
    ('Tiny', 'A', '12', "[!] Error: ISBN '12' is too short."),
    ('First', 'B', '12345', "[!] Error: A book with ISBN 12345 already exists."),
    ('New Book', 'C', 'ABC123', "Success: Added 'New Book' to the library.")
])
def test_add_book(capsys, title, author, isbn, expected, monkeypatch):
    library = LibraryManager()
    if isbn == '12345':
        library.inventory = {'12345': Book('First', 'B', '12345')}
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert expected in captured.out

@pytest.mark.parametrize('isbn, pre_inventory, expected', [
    ('NONEXIST', {}, "[!] Error: Book with ISBN NONEXIST not found."),
    ('111', {'111': Book('Locked', 'D', '111')}, "[!] Unavailable: 'Locked' is currently borrowed by someone else."),
    ('222', {'222': Book('Open', 'E', '222')}, "Success: You have borrowed 'Open'.")
])
def test_borrow_book(capsys, isbn, pre_inventory, expected, monkeypatch):
    library = LibraryManager()
    library.inventory = pre_inventory
    if isbn == '111':
        library.inventory['111'].is_available = False
    library.borrow_book(isbn)
    captured = capsys.readouterr()
    assert expected in captured.out

@pytest.mark.parametrize('isbn, pre_inventory, expected', [
    ('UNKNOWN', {}, "[!] Error: We do not own a book with ISBN UNKNOWN."),
    ('333', {'333': Book('Idle', 'F', '333')}, "[!] Strange: You are trying to return 'Idle', but it was already here."),
    ('444', {'444': Book('Read', 'G', '444')}, "Success: 'Read' has been returned.")
])
def test_return_book(capsys, isbn, pre_inventory, expected, monkeypatch):
    library = LibraryManager()
    library.inventory = pre_inventory
    if isbn == '444':
        library.inventory['444'].is_available = False
    library.return_book(isbn)
    captured = capsys.readouterr()
    assert expected in captured.out

@pytest.mark.parametrize('title, author, isbn, is_available, expected', [
    ('Sample', 'H', '555', True, "[Available] Sample by H (ISBN: 555)"),
    ('Sample', 'H', '555', False, "[Borrowed] Sample by H (ISBN: 555)")
])
def test_book_str(title, author, isbn, is_available, expected):
    book = Book(title, author, isbn)
    book.is_available = is_available
    assert str(book) == expected

@pytest.mark.parametrize('pre_inventory, expected', [
    ({}, "\n--- Current Library Inventory ---\nThe library is empty.\n---------------------------------\n"),
    ({'777': Book('Alpha', 'I', '777'), '888': Book('Beta', 'J', '888')}, "\n--- Current Library Inventory ---\n[Available] Alpha by I (ISBN: 777)\n[Available] Beta by J (ISBN: 888)\n---------------------------------\n")
])
def test_show_inventory(capsys, pre_inventory, expected, monkeypatch):
    library = LibraryManager()
    library.inventory = pre_inventory
    library.show_inventory()
    captured = capsys.readouterr()
    assert expected in captured.out