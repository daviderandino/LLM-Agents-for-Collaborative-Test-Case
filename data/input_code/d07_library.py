class Book:
    """
    Represents a single book.
    It holds the title, author, and the current status (available or borrowed).
    """
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        # By default, a new book is available
        self.is_available = True

    def __str__(self):
        # Helper to print book details nicely
        status = "Available" if self.is_available else "Borrowed"
        return f"[{status}] {self.title} by {self.author} (ISBN: {self.isbn})"


class LibraryManager:
    """
    Manages the collection of books.
    """
    def __init__(self):
        # We use a dictionary for the inventory because it's faster to find books by ISBN.
        # Format: { 'isbn_code': BookObject }
        self.inventory = {}

    def add_book(self, title, author, isbn):
        """Adds a new book to the library."""
        # CHECK 1: Input validation
        if len(isbn) < 3:
            print(f"[!] Error: ISBN '{isbn}' is too short.")
            return

        # CHECK 2: Duplicate validation
        if isbn in self.inventory:
            print(f"[!] Error: A book with ISBN {isbn} already exists.")
            return

        new_book = Book(title, author, isbn)
        self.inventory[isbn] = new_book
        print(f"Success: Added '{title}' to the library.")

    def borrow_book(self, isbn):
        """Attempts to borrow a book."""
        # CHECK 1: Does the book exist?
        if isbn not in self.inventory:
            print(f"[!] Error: Book with ISBN {isbn} not found.")
            return

        book = self.inventory[isbn]

        # CHECK 2: Is the book actually available?
        if not book.is_available:
            print(f"[!] Unavailable: '{book.title}' is currently borrowed by someone else.")
            return

        # LOGIC: Update status
        book.is_available = False
        print(f"Success: You have borrowed '{book.title}'.")

    def return_book(self, isbn):
        """Returns a book to the library."""
        # CHECK 1: Does the book exist?
        if isbn not in self.inventory:
            print(f"[!] Error: We do not own a book with ISBN {isbn}.")
            return

        book = self.inventory[isbn]

        # CHECK 2: Was it borrowed? (Logic consistency check)
        if book.is_available:
            print(f"[!] Strange: You are trying to return '{book.title}', but it was already here.")
            return

        # LOGIC: Update status
        book.is_available = True
        print(f"Success: '{book.title}' has been returned.")

    def show_inventory(self):
        """Prints all books and their status."""
        print("\n--- Current Library Inventory ---")
        if not self.inventory:
            print("The library is empty.")
        else:
            for book in self.inventory.values():
                print(book)
        print("---------------------------------\n")
