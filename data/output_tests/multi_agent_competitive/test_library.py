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

@pytest.mark.parametrize('title, author, isbn, is_available, expected', [
    ("1984", "George Orwell", "9780451524935", True, "[Available] 1984 by George Orwell (ISBN: 9780451524935)")
])
def test_book_str(title, author, isbn, is_available, expected):
    book = Book(title, author, isbn)
    book.is_available = is_available
    assert str(book) == expected

def test_library_manager_init():
    library = LibraryManager()
    assert library.inventory == {}

@pytest.mark.parametrize('title, author, isbn, inventory, expected_inventory', [
    ("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", {}, {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")})
])
def test_library_manager_add_book(title, author, isbn, inventory, expected_inventory):
    library = LibraryManager()
    library.inventory = inventory
    library.add_book(title, author, isbn)
    for key, value in expected_inventory.items():
        assert key in library.inventory
        assert library.inventory[key].title == value.title
        assert library.inventory[key].author == value.author
        assert library.inventory[key].isbn == value.isbn

@pytest.mark.parametrize('isbn, inventory', [
    ("123", {}),
    ("9780743273565", {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")})
])
def test_library_manager_add_book_invalid_isbn(isbn, inventory):
    library = LibraryManager()
    library.inventory = inventory
    library.add_book("title", "author", isbn)
    if len(isbn) < 3:
        assert isbn not in library.inventory

@pytest.mark.parametrize('isbn, inventory', [
    ("9780743273565", {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")})
])
def test_library_manager_borrow_book(isbn, inventory):
    library = LibraryManager()
    library.inventory = inventory
    library.borrow_book(isbn)
    if isbn in inventory:
        assert library.inventory[isbn].is_available == False

@pytest.mark.parametrize('isbn, inventory', [
    ("9780743273565", {}),
    ("9780743273565", {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")})
])
def test_library_manager_borrow_book_not_found(isbn, inventory):
    library = LibraryManager()
    library.inventory = inventory
    library.borrow_book(isbn)
    if isbn not in inventory:
        assert isbn not in library.inventory or library.inventory[isbn].is_available == True

@pytest.mark.parametrize('isbn, inventory', [
    ("9780743273565", {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")})
])
def test_library_manager_return_book(isbn, inventory):
    library = LibraryManager()
    library.inventory = inventory
    library.inventory[isbn].is_available = False
    library.return_book(isbn)
    assert library.inventory[isbn].is_available == True

@pytest.mark.parametrize('isbn, inventory', [
    ("9780743273565", {}),
    ("9780743273565", {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")})
])
def test_library_manager_return_book_not_found(isbn, inventory):
    library = LibraryManager()
    library.inventory = inventory
    library.return_book(isbn)
    if isbn not in inventory:
        assert isbn not in library.inventory or library.inventory[isbn].is_available == True

@pytest.mark.parametrize('inventory', [
    ({}),
    ({"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")})
])
def test_library_manager_show_inventory(inventory, capsys):
    library = LibraryManager()
    library.inventory = inventory
    library.show_inventory()
    captured = capsys.readouterr()
    assert "--- Current Library Inventory ---" in captured.out
    if not inventory:
        assert "The library is empty." in captured.out
    else:
        for book in inventory.values():
            assert str(book) in captured.out

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("To Kill a Mockingbird", "Harper Lee", "9780061120084", None)
])
def test_book_init_new(title, author, isbn, expected):
    book = Book(title, author, isbn)
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn
    assert book.is_available == True

@pytest.mark.parametrize('title, author, isbn, is_available, expected', [
    ("1984", "George Orwell", "9780451524935", True, "[Available] 1984 by George Orwell (ISBN: 9780451524935)")
])
def test_book_str_new(title, author, isbn, is_available, expected):
    book = Book(title, author, isbn)
    book.is_available = is_available
    assert str(book) == expected

def test_library_manager_init_new():
    library = LibraryManager()
    assert library.inventory == {}

@pytest.mark.parametrize('title, author, isbn, inventory, expected', [
    ("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", {}, None)
])
def test_library_manager_add_book_new(title, author, isbn, inventory, expected):
    library = LibraryManager()
    library.inventory = inventory
    library.add_book(title, author, isbn)
    assert isbn in library.inventory

@pytest.mark.parametrize('title, author, isbn, inventory', [
    ("Pride and Prejudice", "Jane Austen", "123", {})
])
def test_library_manager_add_book_isbn_too_short_new(title, author, isbn, inventory):
    library = LibraryManager()
    library.inventory = inventory
    library.add_book(title, author, isbn)
    # ISBN length 3 is considered valid in the current implementation
    assert isbn in library.inventory

@pytest.mark.parametrize('title, author, isbn, inventory', [
    ("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")})
])
def test_library_manager_add_book_duplicate_new(title, author, isbn, inventory):
    library = LibraryManager()
    library.inventory = inventory
    library.add_book(title, author, isbn)
    assert len(library.inventory) == len(inventory)

@pytest.mark.parametrize('isbn, inventory', [
    ("9780743273565", {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")})
])
def test_library_manager_borrow_book_new(isbn, inventory):
    library = LibraryManager()
    library.inventory = inventory
    library.inventory[isbn].is_available = True
    library.borrow_book(isbn)
    assert library.inventory[isbn].is_available == False

@pytest.mark.parametrize('isbn, inventory', [
    ("9780743273565", {})
])
def test_library_manager_borrow_book_not_found_new(isbn, inventory):
    library = LibraryManager()
    library.inventory = inventory
    library.borrow_book(isbn)
    assert isbn not in library.inventory

@pytest.mark.parametrize('isbn, inventory', [
    ("9780743273565", {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")})
])
def test_library_manager_borrow_book_unavailable_new(isbn, inventory):
    library = LibraryManager()
    library.inventory = inventory
    library.inventory[isbn].is_available = False
    library.borrow_book(isbn)
    assert library.inventory[isbn].is_available == False

@pytest.mark.parametrize('isbn, inventory', [
    ("9780743273565", {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")})
])
def test_library_manager_return_book_new(isbn, inventory):
    library = LibraryManager()
    library.inventory = inventory
    library.inventory[isbn].is_available = False
    library.return_book(isbn)
    assert library.inventory[isbn].is_available == True

@pytest.mark.parametrize('isbn, inventory', [
    ("9780743273565", {})
])
def test_library_manager_return_book_not_found_new(isbn, inventory):
    library = LibraryManager()
    library.inventory = inventory
    library.return_book(isbn)
    assert isbn not in library.inventory

@pytest.mark.parametrize('isbn, inventory', [
    ("9780743273565", {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")})
])
def test_library_manager_return_book_already_available_new(isbn, inventory):
    library = LibraryManager()
    library.inventory = inventory
    library.inventory[isbn].is_available = True
    library.return_book(isbn)
    assert library.inventory[isbn].is_available == True

@pytest.mark.parametrize('inventory', [
    ({})
])
def test_library_manager_show_inventory_empty_new(inventory, capsys):
    library = LibraryManager()
    library.inventory = inventory
    library.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

@pytest.mark.parametrize('inventory', [
    ({"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")})
])
def test_library_manager_show_inventory_not_empty_new(inventory, capsys):
    library = LibraryManager()
    library.inventory = inventory
    library.show_inventory()
    captured = capsys.readouterr()
    for book in inventory.values():
        assert str(book) in captured.out

@pytest.mark.parametrize('title, author, isbn, inventory', [
    ("title", "author", "9780743273565", {"9780743273565": Book("existing", "book", "9780743273565")})
])
def test_library_manager_add_book_duplicate_isbn_new(title, author, isbn, inventory):
    library = LibraryManager()
    library.inventory = inventory
    library.add_book(title, author, isbn)
    assert len(library.inventory) == len(inventory)

@pytest.mark.parametrize('isbn, inventory', [
    ("9780743273565", {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")})
])
def test_library_manager_borrow_book_already_borrowed_new(isbn, inventory):
    library = LibraryManager()
    library.inventory = inventory
    library.inventory[isbn].is_available = False
    library.borrow_book(isbn)
    assert library.inventory[isbn].is_available == False

@pytest.mark.parametrize('isbn, inventory', [
    ("9780743273565", {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")})
])
def test_library_manager_return_book_already_available_new(isbn, inventory):
    library = LibraryManager()
    library.inventory = inventory
    library.inventory[isbn].is_available = True
    library.return_book(isbn)
    assert library.inventory[isbn].is_available == True

@pytest.mark.parametrize('title, author, isbn', [
    ("", "author", "9780743273565")
])
def test_library_manager_add_book_empty_title_new(title, author, isbn):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    # Current implementation does not validate empty title
    assert isbn in library.inventory

@pytest.mark.parametrize('title, author, isbn', [
    ("title", "", "9780743273565")
])
def test_library_manager_add_book_empty_author_new(title, author, isbn):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    # Current implementation does not validate empty author
    assert isbn in library.inventory

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("To Kill a Mockingbird", "Harper Lee", "9780061120084", None)
])
def test_book_init_new_1(title, author, isbn, expected):
    book = Book(title, author, isbn)
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn
    assert book.is_available == True

@pytest.mark.parametrize('self_dict, expected', [
    ({"title": "1984", "author": "George Orwell", "isbn": "9780451524935", "is_available": True}, "[Available] 1984 by George Orwell (ISBN: 9780451524935)")
])
def test_book_str_new_1(self_dict, expected):
    book = Book(self_dict['title'], self_dict['author'], self_dict['isbn'])
    book.is_available = self_dict['is_available']
    assert str(book) == expected

@pytest.mark.parametrize('input_dict, expected', [
    ({}, {"inventory": {}})
])
def test_library_manager_init_new_1(input_dict, expected):
    library = LibraryManager()
    assert library.inventory == expected['inventory']

@pytest.mark.parametrize('self_dict, title, author, isbn, expected', [
    ({"inventory": {}}, "The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", None)
])
def test_library_manager_add_book_new_1(self_dict, title, author, isbn, expected):
    library = LibraryManager()
    library.inventory = self_dict['inventory']
    library.add_book(title, author, isbn)
    assert isbn in library.inventory

@pytest.mark.parametrize('self_dict, title, author, isbn, expected', [
    ({"inventory": {}}, "Pride and Prejudice", "Jane Austen", "12", None)
])
def test_library_manager_add_book_isbn_too_short_new_1(self_dict, title, author, isbn, expected):
    library = LibraryManager()
    library.inventory = self_dict['inventory']
    library.add_book(title, author, isbn)
    assert isbn not in library.inventory

@pytest.mark.parametrize('self_dict, title, author, isbn, expected', [
    ({"inventory": {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")}}, "The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", None)
])
def test_library_manager_add_book_duplicate_new_1(self_dict, title, author, isbn, expected):
    library = LibraryManager()
    library.inventory = self_dict['inventory']
    library.add_book(title, author, isbn)
    assert len(library.inventory) == len(self_dict['inventory'])

@pytest.mark.parametrize('self_dict, isbn, expected', [
    ({"inventory": {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565",)}}, "9780743273565", None)
])
def test_library_manager_borrow_book_new_1(self_dict, isbn, expected):
    library = LibraryManager()
    library.inventory = self_dict['inventory']
    library.borrow_book(isbn)
    assert library.inventory[isbn].is_available == False

@pytest.mark.parametrize('self_dict, isbn, expected', [
    ({"inventory": {}}, "9780743273565", None)
])
def test_library_manager_borrow_book_not_found_new_1(self_dict, isbn, expected):
    library = LibraryManager()
    library.inventory = self_dict['inventory']
    library.borrow_book(isbn)
    assert isbn not in library.inventory

@pytest.mark.parametrize('self_dict, isbn, expected', [
    ({"inventory": {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565",)}}, "9780743273565", None)
])
def test_library_manager_borrow_book_unavailable_new_1(self_dict, isbn, expected):
    library = LibraryManager()
    library.inventory = self_dict['inventory']
    library.inventory[isbn].is_available = False
    library.borrow_book(isbn)
    assert library.inventory[isbn].is_available == False

@pytest.mark.parametrize('self_dict, isbn, expected', [
    ({"inventory": {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565",)}}, "9780743273565", None)
])
def test_library_manager_return_book_new_1(self_dict, isbn, expected):
    library = LibraryManager()
    library.inventory = self_dict['inventory']
    library.inventory[isbn].is_available = False
    library.return_book(isbn)
    assert library.inventory[isbn].is_available == True

@pytest.mark.parametrize('self_dict, isbn, expected', [
    ({"inventory": {}}, "9780743273565", None)
])
def test_library_manager_return_book_not_found_new_1(self_dict, isbn, expected):
    library = LibraryManager()
    library.inventory = self_dict['inventory']
    library.return_book(isbn)
    assert isbn not in library.inventory

@pytest.mark.parametrize('self_dict, isbn, expected', [
    ({"inventory": {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565",)}}, "9780743273565", None)
])
def test_library_manager_return_book_already_available_new_1(self_dict, isbn, expected):
    library = LibraryManager()
    library.inventory = self_dict['inventory']
    library.inventory[isbn].is_available = True
    library.return_book(isbn)
    assert library.inventory[isbn].is_available == True

@pytest.mark.parametrize('self_dict', [
    ({"inventory": {}})
])
def test_library_manager_show_inventory_empty_new_1(self_dict, capsys):
    library = LibraryManager()
    library.inventory = self_dict['inventory']
    library.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

@pytest.mark.parametrize('self_dict', [
    ({"inventory": {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")}})
])
def test_library_manager_show_inventory_not_empty_new_1(self_dict, capsys):
    library = LibraryManager()
    library.inventory = self_dict['inventory']
    library.show_inventory()
    captured = capsys.readouterr()
    for book in self_dict['inventory'].values():
        assert str(book) in captured.out

@pytest.mark.parametrize('title, author, isbn', [
    ("title", "author", "9780743273565")
])
def test_library_manager_add_book_duplicate_isbn_new_1(title, author, isbn):
    library = LibraryManager()
    library.add_book("existing", "book", isbn)
    library.add_book(title, author, isbn)
    assert len(library.inventory) == 1

@pytest.mark.parametrize('isbn, inventory_dict', [
    ("9780743273565", {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")})
])
def test_library_manager_borrow_book_already_borrowed_new_1(isbn, inventory_dict):
    library = LibraryManager()
    library.inventory = inventory_dict
    library.inventory[isbn].is_available = False
    library.borrow_book(isbn)
    assert library.inventory[isbn].is_available == False

@pytest.mark.parametrize('isbn, inventory_dict', [
    ("9780743273565", {"9780743273565": Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")})
])
def test_library_manager_return_book_already_available_new_1(isbn, inventory_dict):
    library = LibraryManager()
    library.inventory = inventory_dict
    library.inventory[isbn].is_available = True
    library.return_book(isbn)
    assert library.inventory[isbn].is_available == True

@pytest.mark.parametrize('title, author, isbn', [
    ("", "author", "9780743273565")
])
def test_library_manager_add_book_empty_title_new_1(title, author, isbn):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    assert isbn in library.inventory

@pytest.mark.parametrize('title, author, isbn', [
    ("title", "", "9780743273565")
])
def test_library_manager_add_book_empty_author_new_1(title, author, isbn):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    assert isbn in library.inventory

@pytest.mark.parametrize('title, author, isbn', [
    ("title", "author", "123")
])
def test_library_manager_add_book_isbn_exact_length_new_1(title, author, isbn):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    assert isbn in library.inventory