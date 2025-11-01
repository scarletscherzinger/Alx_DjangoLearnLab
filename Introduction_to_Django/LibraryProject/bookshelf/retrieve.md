# Retrieve Operation

## Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(f"Retrieved Book: {book.title} by {book.author}, published in {book.publication_year}")
```

## Output
```
Retrieved Book: 1984 by George Orwell, published in 1949
```

## Explanation
Retrieved the book with title "1984" from the database and displayed all its attributes (title, author, publication_year).