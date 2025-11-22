from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API view to retrieve list of books.
    Extends ListAPIView to provide GET method handler.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer