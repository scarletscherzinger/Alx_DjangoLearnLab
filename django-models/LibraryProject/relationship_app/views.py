from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book
from .models import Library


# Function-based view to list all books
def list_books(request):
    """Function-based view that lists all books in the database."""
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)


# Class-based view to display library details
class LibraryDetailView(DetailView):
    """Class-based view that displays details of a specific library."""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'