from django.contrib import admin
from .models import Author, Book

# Register the Author model with Django admin
admin.site.register(Author)

# Register the Book model with Django admin
admin.site.register(Book)