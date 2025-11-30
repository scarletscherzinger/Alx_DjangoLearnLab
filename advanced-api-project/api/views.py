from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer


# ListView - Retrieve all books
# Allows anyone to view the list of books (read-only for unauthenticated users)
class BookListView(generics.ListAPIView):
    """
    API view to retrieve a list of all books.
    - GET: Returns a list of all book instances
    - Permissions: Read-only access for all users (authenticated and unauthenticated)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Anyone can read, only authenticated can modify


# DetailView - Retrieve a single book by ID
# Allows anyone to view a specific book's details
class BookDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single book by its ID.
    - GET: Returns details of a specific book
    - Permissions: Read-only access for all users (authenticated and unauthenticated)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Anyone can read


# CreateView - Add a new book
# Only authenticated users can create new books
class BookCreateView(generics.CreateAPIView):
    """
    API view to create a new book.
    - POST: Creates a new book instance
    - Permissions: Only authenticated users can create books
    - Handles form submissions and validates data using BookSerializer
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create

    def perform_create(self, serializer):
        """
        Custom method to handle additional logic during book creation.
        Can be extended to add user tracking, logging, etc.
        """
        # Save the book instance with any additional custom logic
        serializer.save()


# UpdateView - Modify an existing book
# Only authenticated users can update books
class BookUpdateView(generics.UpdateAPIView):
    """
    API view to update an existing book.
    - PUT: Completely updates a book instance
    - PATCH: Partially updates a book instance
    - Permissions: Only authenticated users can update books
    - Validates data using BookSerializer before updating
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can update

    def perform_update(self, serializer):
        """
        Custom method to handle additional logic during book updates.
        Can be extended to add validation, notifications, etc.
        """
        # Save the updated book instance with any additional custom logic
        serializer.save()


# DeleteView - Remove a book
# Only authenticated users can delete books
class BookDeleteView(generics.DestroyAPIView):
    """
    API view to delete a book.
    - DELETE: Removes a book instance from the database
    - Permissions: Only authenticated users can delete books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can delete
