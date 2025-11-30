from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

urlpatterns = [
    # List all books - GET request
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Create a new book - POST request
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    
    # Retrieve a single book by ID - GET request
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Update an existing book - PUT/PATCH request
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),
    
    # Delete a book - DELETE request
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),
]