import pytest
from data.input_code.d07_library import *

@pytest.mark.parametrize("test_case", [
    ("show_inventory_non_empty", 
     ["Test Book", "Test Author", "1234567890"], 
     ["Success: Added 'Test Book' to the library.", 
      "", 
      "--- Current Library Inventory ---", 
      "[Available] Test Book by Test Author (ISBN: 1234567890)", 
      "---------------------------------"]),
    ("add_book_duplicate_isbn", 
     ["Test Book", "Test Author", "1234567890", "Test Book 2", "Test Author 2", "1234567890"], 
     ["Success: Added 'Test Book' to the library.", 
      "[!] Error: A book with ISBN 1234567890 already exists."]),
    ("add_book_invalid_isbn", 
     ["Test Book", "Test Author", "12"], 
     ["[!] Error: ISBN '12' is too short."]),
    ("borrow_book_available", 
     ["Test Book", "Test Author", "1234567890"], 
     ["Success: Added 'Test Book' to the library.", 
      "Success: You have borrowed 'Test Book'."]),
    ("borrow_book_unavailable", 
     ["Test Book", "Test Author", "1234567890"], 
     ["Success: Added 'Test Book' to the library.", 
      "Success: You have borrowed 'Test Book'.", 
      "[!] Unavailable: 'Test Book' is currently borrowed by someone else."]),
    ("return_book_borrowed", 
     ["Test Book", "Test Author", "1234567890"], 
     ["Success: Added 'Test Book' to the library.", 
      "Success: You have borrowed 'Test Book'.", 
      "Success: 'Test Book' has been returned."]),
    ("return_book_already_available", 
     ["Test Book", "Test Author", "1234567890"], 
     ["Success: Added 'Test Book' to the library.", 
      "[!] Strange: You are trying to return 'Test Book', but it was already here."]),
    ("show_inventory_empty", 
     [], 
     ["--- Current Library Inventory ---", 
      "The library is empty.", 
      "---------------------------------"]),
    ("borrow_book_not_found", 
     ["1234567890"], 
     ["[!] Error: Book with ISBN 1234567890 not found."]),
    ("return_book_not_found", 
     ["1234567890"], 
     ["[!] Error: We do not own a book with ISBN 1234567890."])
])
def test_library_manager(capsys, test_case):
    library = LibraryManager()
    if test_case[0] == "show_inventory_non_empty":
        library.add_book(*test_case[1])
        library.show_inventory()
    elif test_case[0] == "add_book_duplicate_isbn":
        library.add_book(*test_case[1][:3])
        library.add_book(*test_case[1][3:])
    elif test_case[0] == "add_book_invalid_isbn":
        library.add_book(*test_case[1])
    elif test_case[0] == "borrow_book_available":
        library.add_book(*test_case[1][:3])
        library.borrow_book(test_case[1][2])
    elif test_case[0] == "borrow_book_unavailable":
        library.add_book(*test_case[1][:3])
        library.borrow_book(test_case[1][2])
        library.borrow_book(test_case[1][2])
    elif test_case[0] == "return_book_borrowed":
        library.add_book(*test_case[1][:3])
        library.borrow_book(test_case[1][2])
        library.return_book(test_case[1][2])
    elif test_case[0] == "return_book_already_available":
        library.add_book(*test_case[1])
        library.return_book(test_case[1][2])
    elif test_case[0] == "show_inventory_empty":
        library.show_inventory()
    elif test_case[0] == "borrow_book_not_found":
        library.borrow_book(test_case[1][0])
    elif test_case[0] == "return_book_not_found":
        library.return_book(test_case[1][0])

    captured = capsys.readouterr()
    output = captured.out.strip().split('\n')
    assert output == test_case[2]