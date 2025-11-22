from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API view to retrieve list of books.
    Extends ListAPIView to provide GET method handler.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

 
class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Book model.
    Provides list, create, retrieve, update, and destroy actions.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer 
    permission_classes = [IsAuthenticated]   