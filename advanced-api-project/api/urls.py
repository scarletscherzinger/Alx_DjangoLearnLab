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
    
    # Retrieve a single book by ID - GET request
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Create a new book - POST request
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    
    # Update an existing book - PUT/PATCH request
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    
    # Delete a book - DELETE request
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]