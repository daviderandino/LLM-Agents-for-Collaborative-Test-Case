import pytest
from unittest.mock import patch
from data.input_code.library import Book, LibraryManager

def test_book_initialization():
    book = Book("Title", "Author", "1234567890")
    assert book.title == "Title"
    assert book.author == "Author"
    assert book.isbn == "1234567890"
    assert book.is_available == True

def test_book_str_representation():
    book = Book("Title", "Author", "1234567890")
    assert str(book) == "[Available] Title by Author (ISBN: 1234567890)"
    book.is_available = False
    assert str(book) == "[Borrowed] Title by Author (ISBN: 1234567890)"

def test_library_manager_initialization():
    library = LibraryManager()
    assert library.inventory == {}

def test_add_book_valid():
    library = LibraryManager()
    with patch('builtins.print') as mock_print:
        library.add_book("Title", "Author", "1234567890")
        assert "1234567890" in library.inventory
        mock_print.assert_called_with("Success: Added 'Title' to the library.")

def test_add_book_isbn_too_short():
    library = LibraryManager()
    with patch('builtins.print') as mock_print:
        library.add_book("Title", "Author", "12")
        assert "12" not in library.inventory
        mock_print.assert_called_with("[!] Error: ISBN '12' is too short.")

def test_add_book_duplicate_isbn():
    library = LibraryManager()
    with patch('builtins.print') as mock_print:
        library.add_book("Title1", "Author1", "1234567890")
        library.add_book("Title2", "Author2", "1234567890")
        assert len(library.inventory) == 1
        mock_print.assert_called_with("[!] Error: A book with ISBN 1234567890 already exists.")

def test_borrow_book_valid():
    library = LibraryManager()
    library.add_book("Title", "Author", "1234567890")
    with patch('builtins.print') as mock_print:
        library.borrow_book("1234567890")
        book = library.inventory["1234567890"]
        assert not book.is_available
        mock_print.assert_called_with("Success: You have borrowed 'Title'.")

def test_borrow_book_not_found():
    library = LibraryManager()
    with patch('builtins.print') as mock_print:
        library.borrow_book("1234567890")
        mock_print.assert_called_with("[!] Error: Book with ISBN 1234567890 not found.")

def test_borrow_book_already_borrowed():
    library = LibraryManager()
    library.add_book("Title", "Author", "1234567890")
    library.borrow_book("1234567890")
    with patch('builtins.print') as mock_print:
        library.borrow_book("1234567890")
        mock_print.assert_called_with("[!] Unavailable: 'Title' is currently borrowed by someone else.")

def test_return_book_valid():
    library = LibraryManager()
    library.add_book("Title", "Author", "1234567890")
    library.borrow_book("1234567890")
    with patch('builtins.print') as mock_print:
        library.return_book("1234567890")
        book = library.inventory["1234567890"]
        assert book.is_available
        mock_print.assert_called_with("Success: 'Title' has been returned.")

def test_return_book_not_found():
    library = LibraryManager()
    with patch('builtins.print') as mock_print:
        library.return_book("1234567890")
        mock_print.assert_called_with("[!] Error: We do not own a book with ISBN 1234567890.")

def test_return_book_already_returned():
    library = LibraryManager()
    library.add_book("Title", "Author", "1234567890")
    with patch('builtins.print') as mock_print:
        library.return_book("1234567890")
        mock_print.assert_called_with("[!] Strange: You are trying to return 'Title', but it was already here.")

def test_show_inventory_empty():
    library = LibraryManager()
    with patch('builtins.print') as mock_print:
        library.show_inventory()
        mock_print.assert_any_call("The library is empty.")

def test_show_inventory_not_empty():
    library = LibraryManager()
    library.add_book("Title", "Author", "1234567890")
    with patch('builtins.print') as mock_print:
        library.show_inventory()
        mock_print.assert_any_call("[Available] Title by Author (ISBN: 1234567890)")