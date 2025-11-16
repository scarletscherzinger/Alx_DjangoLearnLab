# Update Operation

## Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated Book: {book.title} by {book.author}, published in {book.publication_year}")
```

## Output
```
Updated Book: Nineteen Eighty-Four by George Orwell, published in 1949
```

## Explanation
Retrieved the book with title "1984", updated its title to "Nineteen Eighty-Four", saved the changes to the database, and displayed the updated book details.