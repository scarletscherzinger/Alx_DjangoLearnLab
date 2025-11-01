# Delete Operation

## Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print("Book deleted successfully")
# Confirm deletion
all_books = Book.objects.all()
print(f"Total books in database: {all_books.count()}")
```

## Output
```
Book deleted successfully
Total books in database: 0
```

## Explanation
Retrieved the book with title "Nineteen Eighty-Four", deleted it from the database, and confirmed the deletion by checking that no books remain in the database.