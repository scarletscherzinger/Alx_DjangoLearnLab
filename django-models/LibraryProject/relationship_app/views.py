from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
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

# User registration view
def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# User login view - using Django's built-in LoginView
from django.contrib.auth.views import LoginView, LogoutView

# Custom logout view (optional - can also use Django's built-in)
def user_logout(request):
    """Handle user logout."""
    logout(request)
    return render(request, 'relationship_app/logout.html')