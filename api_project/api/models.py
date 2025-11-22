from django.db import models

class Book(models.Model):
    """
    Book model for the API.
    Represents a book with a title and author.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title