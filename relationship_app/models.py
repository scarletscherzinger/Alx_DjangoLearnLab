from django.db import models
from django.conf import settings  # Import settings for custom user reference

class Author(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_year = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class Library(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Librarian(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    favorite_books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.user.username
