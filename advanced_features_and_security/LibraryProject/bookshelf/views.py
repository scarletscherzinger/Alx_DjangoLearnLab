from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from .models import Book
from .forms import ExampleForm

# Secure view using Django ORM to prevent SQL injection
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Display list of books using Django ORM (prevents SQL injection).
    Searches are parameterized through ORM.
    """
    search_query = request.GET.get('search', '')
    
    if search_query:
        # Safe: Django ORM parameterizes queries automatically
        books = Book.objects.filter(title__icontains=search_query)
    else:
        books = Book.objects.all()
    
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """Create a new book with secure form handling"""
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        
        # Django ORM prevents SQL injection
        Book.objects.create(title=title, author=author, publication_year=publication_year)
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_form.html')

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """Edit a book with secure form handling"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.publication_year = request.POST.get('publication_year')
        book.save()
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_form.html', {'book': book})

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """Delete a book with CSRF protection"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

def example_form_view(request):
    """
    Example form view demonstrating secure form handling.
    Uses Django forms for validation and CSRF protection.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process cleaned data (automatically sanitized by Django)
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Process the form data securely
            return HttpResponse(f"Form submitted successfully by {name}")
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})