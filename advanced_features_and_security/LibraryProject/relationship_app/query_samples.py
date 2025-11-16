import django
import os

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query 1: Query all books by a specific author
def books_by_author(author_name):
    """Query all books by a specific author."""
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"Books by {author_name}:")
        for book in books:
            print(f"  - {book.title}")
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")

# Query 2: List all books in a library
def books_in_library(library_name):
    """List all books in a library."""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library_name}:")
        for book in books:
            print(f"  - {book.title}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")

# Query 3: Retrieve the librarian for a library
def librarian_for_library(library_name):
    """Retrieve the librarian for a library."""
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        print(f"Librarian for {library_name}: {librarian.name}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to {library_name}.")

# Example usage (you can test these after adding data to your database)
if __name__ == "__main__":
    # Uncomment these lines after adding some test data
    # books_by_author("J.K. Rowling")
    # books_in_library("Central Library")
    # librarian_for_library("Central Library")
    pass