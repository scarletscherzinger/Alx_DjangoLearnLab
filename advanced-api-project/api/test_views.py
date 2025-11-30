from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Book, Author


class BookAPITestCase(APITestCase):
    """
    Comprehensive test suite for Book API endpoints.
    Tests CRUD operations, filtering, searching, ordering, and permissions.
    """

    def setUp(self):
        """
        Set up test data and authentication for each test.
        This method runs before each test case.
        """
        # Create test users
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )

    def test_list_books(self):
        """
        Test retrieving list of all books.
        Expected: Status 200 OK and correct number of books returned.
        """
        url = reverse('book-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        """
        Test retrieving a single book by ID.
        Expected: Status 200 OK and correct book data returned.
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Harry Potter')
        self.assertEqual(response.data['publication_year'], 1997)

    def test_create_book_authenticated(self):
        """
        Test creating a book with authentication.
        Expected: Status 201 Created and book is saved in database.
        """
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-create')
        data = {
            'title': 'New Book',
            'publication_year': 2020,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.get(id=response.data['id']).title, 'New Book')

    def test_create_book_unauthenticated(self):
        """
        Test creating a book without authentication.
        Expected: Status 403 Forbidden (authentication required).
        """
        url = reverse('book-create')
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2020,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 2)  # No new book created

    def test_update_book_authenticated(self):
        """
        Test updating a book with authentication.
        Expected: Status 200 OK and book data is updated.
        """
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Harry Potter Updated',
            'publication_year': 1997,
            'author': self.author1.id
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Harry Potter Updated')

    def test_update_book_unauthenticated(self):
        """
        Test updating a book without authentication.
        Expected: Status 403 Forbidden (authentication required).
        """
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Unauthorized Update',
            'publication_year': 1997,
            'author': self.author1.id
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_authenticated(self):
        """
        Test deleting a book with authentication.
        Expected: Status 204 No Content and book is removed from database.
        """
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_delete_book_unauthenticated(self):
        """
        Test deleting a book without authentication.
        Expected: Status 403 Forbidden (authentication required).
        """
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 2)  # Book not deleted

    def test_filter_books_by_title(self):
        """
        Test filtering books by title.
        Expected: Status 200 OK and only matching books returned.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'title': 'Harry Potter'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter')

    def test_filter_books_by_author(self):
        """
        Test filtering books by author ID.
        Expected: Status 200 OK and only books by that author returned.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'author': self.author2.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')

    def test_filter_books_by_publication_year(self):
        """
        Test filtering books by publication year.
        Expected: Status 200 OK and only books from that year returned.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'publication_year': 1949})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 1949)

    def test_search_books(self):
        """
        Test searching books by title and author name.
        Expected: Status 200 OK and matching books returned.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'search': 'Orwell'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')

    def test_order_books_by_title(self):
        """
        Test ordering books by title (ascending).
        Expected: Status 200 OK and books ordered alphabetically.
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], '1984')
        self.assertEqual(response.data[1]['title'], 'Harry Potter')

    def test_order_books_by_publication_year_descending(self):
        """
        Test ordering books by publication year (descending).
        Expected: Status 200 OK and books ordered by year (newest first).
        """
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 1997)
        self.assertEqual(response.data[1]['publication_year'], 1949)

    def test_create_book_invalid_year(self):
        """
        Test creating a book with future publication year.
        Expected: Status 400 Bad Request (validation error).
        """
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-create')
        data = {
            'title': 'Future Book',
            'publication_year': 2030,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)