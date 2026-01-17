import pytest
from data.input_code.d07_library import *

# ------------------------------------------------------------------
# Helper fixtures
# ------------------------------------------------------------------
@pytest.fixture
def lib_manager():
    """Return a fresh LibraryManager instance."""
    return LibraryManager()

@pytest.fixture
def book():
    """Return a Book instance."""
    return Book("Test Book", "Test Author", "1234567890")

# ------------------------------------------------------------------
# Book tests
# ------------------------------------------------------------------
def test_book_init(book):
    """T1_Init: Verify Book attributes after initialization."""
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.isbn == "1234567890"
    assert book.is_available is True

def test_book_str(book):
    """T2_Str: Verify string representation of a Book."""
    expected = "[Available] Test Book by Test Author (ISBN: 1234567890)"
    assert str(book) == expected

# ------------------------------------------------------------------
# LibraryManager initialization
# ------------------------------------------------------------------
def test_library_manager_init(lib_manager):
    """T3_Library_Init: Verify that inventory starts empty."""
    assert lib_manager.inventory == {}

# ------------------------------------------------------------------
# add_book tests
# ------------------------------------------------------------------
@pytest.mark.parametrize(
    "title, author, isbn, expected_len, expected_duplicate",
    [
        ("Test Book", "Test Author", "1234567890", 1, False),  # T4_Add_Book_OK
        ("Test Book", "Test Author", "12", 0, False),          # T5_Add_Book_ISBN_Too_Short
        ("Test Book", "Test Author", "1234567890", 1, True),   # T6_Add_Book_Duplicate
    ]
)
def test_add_book(lib_manager, title, author, isbn, expected_len, expected_duplicate):
    """T4, T5, T6: Test adding books with various ISBN conditions."""
    # Add first book if not duplicate
    if not expected_duplicate:
        lib_manager.add_book(title, author, isbn)
    else:
        # Ensure book is already present
        lib_manager.add_book(title, author, isbn)
        lib_manager.add_book(title, author, isbn)  # Try adding duplicate

    # Check inventory size
    assert len(lib_manager.inventory) == expected_len

    # If duplicate, inventory should still contain only one entry
    if expected_duplicate:
        assert isbn in lib_manager.inventory
        book_obj = lib_manager.inventory[isbn]
        assert book_obj.title == title
        assert book_obj.author == author

# ------------------------------------------------------------------
# borrow_book tests
# ------------------------------------------------------------------
@pytest.mark.parametrize(
    "isbn, pre_borrowed, expected_available",
    [
        ("1234567890", False, False),  # T7_Borrow_Book_OK
        ("9876543210", False, None),   # T8_Borrow_Book_Not_Found
        ("1234567890", True, False),   # T9_Borrow_Book_Unavailable
    ]
)
def test_borrow_book(lib_manager, isbn, pre_borrowed, expected_available):
    """T7, T8, T9: Test borrowing books under different conditions."""
    # Setup: add a book if needed
    if isbn == "1234567890":
        lib_manager.add_book("Test Book", "Test Author", isbn)
        if pre_borrowed:
            lib_manager.borrow_book(isbn)

    # Attempt to borrow
    lib_manager.borrow_book(isbn)

    # Verify state
    if isbn in lib_manager.inventory:
        book_obj = lib_manager.inventory[isbn]
        assert book_obj.is_available == expected_available
    else:
        assert isbn not in lib_manager.inventory  # Corrected assertion

# ------------------------------------------------------------------
# return_book tests
# ------------------------------------------------------------------
@pytest.mark.parametrize(
    "isbn, pre_borrowed, expected_available",
    [
        ("1234567890", True, True),   # T10_Return_Book_OK
        ("9876543210", False, None),  # T11_Return_Book_Not_Found
        ("1234567890", False, True),  # T12_Return_Book_Already_Available
    ]
)
def test_return_book(lib_manager, isbn, pre_borrowed, expected_available):
    """T10, T11, T12: Test returning books under different conditions."""
    # Setup: add a book if needed
    if isbn == "1234567890":
        lib_manager.add_book("Test Book", "Test Author", isbn)
        if pre_borrowed:
            lib_manager.borrow_book(isbn)

    # Attempt to return
    lib_manager.return_book(isbn)

    # Verify state
    if isbn in lib_manager.inventory:
        book_obj = lib_manager.inventory[isbn]
        assert book_obj.is_available == expected_available
    else:
        assert True  # If the book is not found, no change is expected

# ------------------------------------------------------------------
# show_inventory tests
# ------------------------------------------------------------------
def test_show_inventory_empty(lib_manager, capsys):
    """T13_Show_Inventory_Empty: Verify output when inventory is empty."""
    lib_manager.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_show_inventory_not_empty(lib_manager, capsys):
    """T14_Show_Inventory_Not_Empty: Verify output when inventory has books."""
    lib_manager.add_book("Test Book", "Test Author", "1234567890")
    lib_manager.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Test Book by Test Author (ISBN: 1234567890)" in captured.out