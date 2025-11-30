# Advanced API Project - Django REST Framework

## Overview
This project implements a RESTful API for managing books and authors using Django REST Framework with custom views and generic views.

## Models
- **Author**: Represents book authors with a name field
- **Book**: Represents books with title, publication_year, and a foreign key to Author

## API Endpoints

### Book Endpoints

| Endpoint | Method | Description | Authentication Required |
|----------|--------|-------------|------------------------|
| `/api/books/` | GET | List all books | No (Read-only) |
| `/api/books/<id>/` | GET | Retrieve a single book | No (Read-only) |
| `/api/books/create/` | POST | Create a new book | Yes |
| `/api/books/<id>/update/` | PUT/PATCH | Update an existing book | Yes |
| `/api/books/<id>/delete/` | DELETE | Delete a book | Yes |

## Views Configuration

### BookListView
- **Type**: `generics.ListAPIView`
- **Purpose**: Retrieve all books
- **Permissions**: `IsAuthenticatedOrReadOnly` - Anyone can view, only authenticated users can modify
- **Serializer**: `BookSerializer`

### BookDetailView
- **Type**: `generics.RetrieveAPIView`
- **Purpose**: Retrieve a single book by ID
- **Permissions**: `IsAuthenticatedOrReadOnly`
- **Serializer**: `BookSerializer`

### BookCreateView
- **Type**: `generics.CreateAPIView`
- **Purpose**: Create a new book
- **Permissions**: `IsAuthenticated` - Only authenticated users
- **Serializer**: `BookSerializer`
- **Custom Method**: `perform_create()` - Handles additional logic during creation

### BookUpdateView
- **Type**: `generics.UpdateAPIView`
- **Purpose**: Update an existing book (full or partial)
- **Permissions**: `IsAuthenticated` - Only authenticated users
- **Serializer**: `BookSerializer`
- **Custom Method**: `perform_update()` - Handles additional logic during updates

### BookDeleteView
- **Type**: `generics.DestroyAPIView`
- **Purpose**: Delete a book
- **Permissions**: `IsAuthenticated` - Only authenticated users
- **Serializer**: `BookSerializer`

## Permissions

The API implements two permission levels:

1. **IsAuthenticatedOrReadOnly**: Used for list and detail views
   - Unauthenticated users: Read-only access (GET requests)
   - Authenticated users: Full access

2. **IsAuthenticated**: Used for create, update, and delete views
   - Only authenticated users can perform these operations
   - Returns 403 Forbidden for unauthenticated requests

## Custom Validation

The `BookSerializer` includes custom validation:
- **publication_year**: Cannot be in the future (validates against current year)

## Testing

To test the API endpoints:

1. Start the development server:
```bash
   python manage.py runserver
```

2. Run the test script:
```bash
   python test_api.py
```

### Manual Testing with curl

**List all books (no authentication required):**
```bash
curl http://127.0.0.1:8000/api/books/
```

**Get a single book (no authentication required):**
```bash
curl http://127.0.0.1:8000/api/books/1/
```

**Create a book (authentication required):**
```bash
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -d '{"title": "New Book", "publication_year": 2024, "author": 1}'
```

## Setup Instructions

1. Install dependencies:
```bash
   pip install django djangorestframework
```

2. Run migrations:
```bash
   python manage.py makemigrations
   python manage.py migrate
```

3. Create a superuser:
```bash
   python manage.py createsuperuser
```

4. Start the server:
```bash
   python manage.py runserver
```

## Project Structure
```
advanced-api-project/
├── advanced_api_project/
│   ├── settings.py
│   └── urls.py
├── api/
│   ├── models.py          # Author and Book models
│   ├── serializers.py     # BookSerializer and AuthorSerializer
│   ├── views.py           # Generic views for CRUD operations
│   └── urls.py            # API URL patterns
└── manage.py
```