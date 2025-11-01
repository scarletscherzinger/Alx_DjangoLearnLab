# Create Operation

## Command
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(f"Book created: {book.title} by {book.author}, published in {book.publication_year}")
```

## Output
```
Book created: 1984 by George Orwell, published in 1949
```

## Explanation
Created a new Book instance with title "1984", author "George Orwell", and publication year 1949. The book was successfully saved to the database.