import pytest
from data.input_code.d04_library import *

@pytest.mark.parametrize('title, author, isbn, expected', [
    ('Test Book', 'Author', '123456', '[Available] Test Book by Author (ISBN: 123456)'),
    ('Test Book', 'Author', '123456', '[Borrowed] Test Book by Author (ISBN: 123456)'),
])
def test_book_str(title, author, isbn, expected):
    book = Book(title, author, isbn)
    if 'Borrowed' in expected:
        book.is_available = False
    assert str(book) == expected

@pytest.mark.parametrize('title, author, isbn, expected', [
    ('Book1', 'Author1', 'ISBN1', {'inventory_length': 1, 'book_title': 'Book1'}),
    ('Book2', 'Author2', '12', {'inventory_length': 0}),
    ('Book3', 'Author3', 'ISBN3', {'inventory_length': 1}),
])
def test_library_manager_add_book(title, author, isbn, expected):
    library = LibraryManager()
    try:
        library.add_book(title, author, isbn)
    except ValueError:
        assert len(library.inventory) == expected['inventory_length']
    else:
        if 'book_title' in expected:
            assert len(library.inventory) == expected['inventory_length']
            assert list(library.inventory.values())[0].title == expected['book_title']
        else:
            assert len(library.inventory) == expected['inventory_length']

@pytest.mark.parametrize('isbn, expected', [
    ('NONEXIST', {'inventory_length': 2}),
    ('ISBN4', {'is_available': False}),
    ('ISBN5', {'is_available': False}),
])
def test_library_manager_borrow_book(isbn, expected):
    library = LibraryManager()
    library.add_book('Book4', 'Author4', 'ISBN4')
    library.add_book('Book5', 'Author5', 'ISBN5')
    try:
        library.borrow_book(isbn)
    except ValueError:
        assert len(library.inventory) == expected['inventory_length']
    else:
        if 'is_available' in expected:
            if isbn == 'ISBN4':
                assert library.inventory['ISBN4'].is_available == expected['is_available']
            elif isbn == 'ISBN5':
                assert library.inventory['ISBN5'].is_available == expected['is_available']

@pytest.mark.parametrize('isbn, expected', [
    ('NONEXIST', {'inventory_length': 2}),
    ('ISBN6', {'is_available': True}),
    ('ISBN7', {'is_available': True}),
])
def test_library_manager_return_book(isbn, expected):
    library = LibraryManager()
    library.add_book('Book6', 'Author6', 'ISBN6')
    library.add_book('Book7', 'Author7', 'ISBN7')
    library.borrow_book('ISBN7')
    try:
        library.return_book(isbn)
    except ValueError:
        assert len(library.inventory) == expected['inventory_length']
    else:
        if 'is_available' in expected:
            if isbn == 'ISBN6':
                assert library.inventory['ISBN6'].is_available == True
            elif isbn == 'ISBN7':
                assert library.inventory['ISBN7'].is_available == True

@pytest.mark.parametrize('expected', [
    {'inventory_length': 0},
    {'inventory_length': 1},
])
def test_library_manager_show_inventory(expected):
    library = LibraryManager()
    if expected['inventory_length'] == 1:
        library.add_book('Book8', 'Author8', 'ISBN8')
    library.show_inventory()
    assert len(library.inventory) == expected['inventory_length']

@pytest.mark.parametrize('title, author, isbn', [
    ('Duplicate Book', 'Author', 'ISBN_DUP'),
])
def test_library_manager_add_book_duplicate(title, author, isbn):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    library.add_book(title, author, isbn)
    assert len(library.inventory) == 1

@pytest.mark.parametrize('title, author, isbn', [
    ('Book to Borrow', 'Author', 'ISBN_BORROW'),
])
def test_library_manager_borrow_book_already_borrowed(title, author, isbn):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    library.borrow_book(isbn)
    library.borrow_book(isbn)
    assert library.inventory[isbn].is_available == False

@pytest.mark.parametrize('titles, authors, isbns', [
    (['Book1', 'Book2', 'Book3'], ['Author1', 'Author2', 'Author3'], ['ISBN1', 'ISBN2', 'ISBN3']),
])
def test_library_manager_show_inventory_multiple(titles, authors, isbns):
    library = LibraryManager()
    for title, author, isbn in zip(titles, authors, isbns):
        library.add_book(title, author, isbn)
    library.show_inventory()
    assert len(library.inventory) == len(titles)