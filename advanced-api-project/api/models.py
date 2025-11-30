from django.db import models

# Author model to store information about book authors
class Author(models.Model):
    """
    Author model represents a book author.
    An author can have multiple books (one-to-many relationship).
    """
    # Name field to store the author's full name
    name = models.CharField(max_length=200)

    def __str__(self):
        """String representation of the Author model"""
        return self.name


# Book model to store information about books
class Book(models.Model):
    """
    Book model represents a book written by an author.
    Each book is linked to one author through a foreign key relationship.
    """
    # Title field to store the book's title
    title = models.CharField(max_length=200)
    
    # Publication year field to store when the book was published
    publication_year = models.IntegerField()
    
    # Foreign key relationship to Author model
    # This creates a one-to-many relationship (one author can have many books)
    # related_name='books' allows us to access all books by an author using author.books.all()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        """String representation of the Book model"""
        return self.title