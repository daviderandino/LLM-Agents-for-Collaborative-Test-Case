import pytest
from data.input_code.d04_library import Book, LibraryManager

def test_book_str_representation():
    b = Book("1984", "George Orwell", "12345")
    assert str(b) == "[Available] 1984 by George Orwell (ISBN: 12345)"
    b.is_available = False
    assert str(b) == "[Borrowed] 1984 by George Orwell (ISBN: 12345)"

def test_add_book_valid_and_invalid_cases(capsys):
    lib = LibraryManager()
    # Invalid: ISBN too short
    lib.add_book("Short ISBN", "Author", "12")
    out = capsys.readouterr().out
    assert "[!] Error: ISBN '12' is too short." in out
    assert "12" not in lib.inventory

    # Valid addition
    lib.add_book("Valid Book", "Author", "ABC")
    out = capsys.readouterr().out
    assert "Success: Added 'Valid Book' to the library." in out
    assert "ABC" in lib.inventory
    book = lib.inventory["ABC"]
    assert isinstance(book, Book)
    assert book.title == "Valid Book"
    assert book.is_available

    # Duplicate ISBN
    lib.add_book("Another Book", "Author", "ABC")
    out = capsys.readouterr().out
    assert "[!] Error: A book with ISBN ABC already exists." in out
    # inventory unchanged
    assert len(lib.inventory) == 1
    assert lib.inventory["ABC"].title == "Valid Book"

def test_borrow_book_various_paths(capsys):
    lib = LibraryManager()
    lib.add_book("Borrow Me", "Author", "XYZ")
    capsys.readouterr()  # clear

    # Non‑existent ISBN
    lib.borrow_book("NOPE")
    out = capsys.readouterr().out
    assert "[!] Error: Book with ISBN NOPE not found." in out

    # Successful borrow
    lib.borrow_book("XYZ")
    out = capsys.readouterr().out
    assert "Success: You have borrowed 'Borrow Me'." in out
    assert not lib.inventory["XYZ"].is_available

    # Attempt to borrow again (already borrowed)
    lib.borrow_book("XYZ")
    out = capsys.readouterr().out
    assert "[!] Unavailable: 'Borrow Me' is currently borrowed by someone else." in out
    # status unchanged
    assert not lib.inventory["XYZ"].is_available

def test_return_book_various_paths(capsys):
    lib = LibraryManager()
    lib.add_book("Return Me", "Author", "RET")
    capsys.readouterr()  # clear

    # Return non‑existent ISBN
    lib.return_book("NONE")
    out = capsys.readouterr().out
    assert "[!] Error: We do not own a book with ISBN NONE." in out

    # Return when book is already available
    lib.return_book("RET")
    out = capsys.readouterr().out
    assert "[!] Strange: You are trying to return 'Return Me', but it was already here." in out
    assert lib.inventory["RET"].is_available

    # Borrow then return successfully
    lib.borrow_book("RET")
    capsys.readouterr()
    lib.return_book("RET")
    out = capsys.readouterr().out
    assert "Success: 'Return Me' has been returned." in out
    assert lib.inventory["RET"].is_available

def test_show_inventory_empty_and_populated(capsys):
    lib = LibraryManager()
    # Empty inventory
    lib.show_inventory()
    out = capsys.readouterr().out
    assert "The library is empty." in out

    # Populate and check output format
    lib.add_book("Alpha", "A", "111")
    lib.add_book("Beta", "B", "222")
    lib.borrow_book("222")
    capsys.readouterr()
    lib.show_inventory()
    out = capsys.readouterr().out
    # Header and footer present
    assert "--- Current Library Inventory ---" in out
    assert "---------------------------------" in out
    # Book lines
    assert "[Available] Alpha by A (ISBN: 111)" in out
    assert "[Borrowed] Beta by B (ISBN: 222)" in out

def test_add_book_type_error():
    lib = LibraryManager()
    # Passing a non‑string ISBN should raise a TypeError due to len()
    with pytest.raises(TypeError):
        lib.add_book("Bad", "Author", None)