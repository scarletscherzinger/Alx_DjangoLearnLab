# Advanced API Project - Django REST Framework

## Overview
This project implements a RESTful API for managing books and authors using Django REST Framework with custom views, generic views, filtering, searching, and ordering capabilities.

## Models
- **Author**: Represents book authors with a name field
- **Book**: Represents books with title, publication_year, and a foreign key to Author

## API Endpoints

### Book Endpoints

| Endpoint | Method | Description | Authentication Required |
|----------|--------|-------------|------------------------|
| `/api/books/` | GET | List all books (with filtering, searching, ordering) | No (Read-only) |
| `/api/books/<id>/` | GET | Retrieve a single book | No (Read-only) |
| `/api/books/create/` | POST | Create a new book | Yes |
| `/api/books/update/<id>/` | PUT/PATCH | Update an existing book | Yes |
| `/api/books/delete/<id>/` | DELETE | Delete a book | Yes |

## Advanced Query Capabilities

### Filtering
Filter books by specific field values using query parameters.

**Available Filter Fields:**
- `title` - Filter by exact book title
- `author` - Filter by author ID
- `publication_year` - Filter by publication year

**Examples:**
```bash
# Filter by title
GET /api/books/?title=1984

# Filter by author ID
GET /api/books/?author=1

# Filter by publication year
GET /api/books/?publication_year=1949

# Combine multiple filters
GET /api/books/?author=1&publication_year=1997
```

### Searching
Search across multiple fields using a single search query parameter.

**Searchable Fields:**
- `title` - Book title
- `author__name` - Author's name (uses relationship lookup)

**Examples:**
```bash
# Search for books with "Potter" in title or author name
GET /api/books/?search=Potter

# Search for books related to "Orwell"
GET /api/books/?search=Orwell

# Search is case-insensitive and matches partial text
GET /api/books/?search=harry
```

### Ordering
Sort results by specific fields in ascending or descending order.

**Available Ordering Fields:**
- `title` - Order by book title
- `publication_year` - Order by publication year

**Examples:**
```bash
# Order by title (ascending, A-Z)
GET /api/books/?ordering=title

# Order by title (descending, Z-A)
GET /api/books/?ordering=-title

# Order by publication year (oldest first)
GET /api/books/?ordering=publication_year

# Order by publication year (newest first)
GET /api/books/?ordering=-publication_year
```

**Note:** Use `-` prefix for descending order.

### Combining Features
You can combine filtering, searching, and ordering in a single request:
```bash
# Search for "Harry", filter by year, and order by title
GET /api/books/?search=Harry&publication_year=1997&ordering=title

# Filter by author and order by publication year (newest first)
GET /api/books/?author=1&ordering=-publication_year
```

## Views Configuration

### BookListView
- **Type**: `generics.ListAPIView`
- **Purpose**: Retrieve all books with advanced query capabilities
- **Permissions**: `IsAuthenticatedOrReadOnly`
- **Features**:
  - **Filtering**: Uses `DjangoFilterBackend` to filter by title, author, and publication_year
  - **Searching**: Uses `SearchFilter` to search across title and author name fields
  - **Ordering**: Uses `OrderingFilter` to sort by title or publication_year
- **Filter Backends**: 
  - `DjangoFilterBackend` - Enables precise field-based filtering
  - `SearchFilter` - Enables text-based searching across multiple fields
  - `OrderingFilter` - Enables result sorting
- **Filterset Fields**: `['title', 'author', 'publication_year']`
- **Search Fields**: `['title', 'author__name']`
- **Ordering Fields**: `['title', 'publication_year']`
- **Default Ordering**: Books are ordered by title in ascending order

### BookDetailView
- **Type**: `generics.RetrieveAPIView`
- **Purpose**: Retrieve a single book by ID
- **Permissions**: `IsAuthenticatedOrReadOnly`

### BookCreateView
- **Type**: `generics.CreateAPIView`
- **Purpose**: Create a new book
- **Permissions**: `IsAuthenticated` - Only authenticated users
- **Custom Method**: `perform_create()` - Handles additional logic during creation

### BookUpdateView
- **Type**: `generics.UpdateAPIView`
- **Purpose**: Update an existing book (full or partial)
- **Permissions**: `IsAuthenticated` - Only authenticated users
- **Custom Method**: `perform_update()` - Handles additional logic during updates

### BookDeleteView
- **Type**: `generics.DestroyAPIView`
- **Purpose**: Delete a book
- **Permissions**: `IsAuthenticated` - Only authenticated users

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

### Testing with curl

**List all books:**
```bash
curl http://127.0.0.1:8000/api/books/
```

**Filter by publication year:**
```bash
curl "http://127.0.0.1:8000/api/books/?publication_year=1949"
```

**Search for books:**
```bash
curl "http://127.0.0.1:8000/api/books/?search=Orwell"
```

**Order by title (descending):**
```bash
curl "http://127.0.0.1:8000/api/books/?ordering=-title"
```

**Combine filters, search, and ordering:**
```bash
curl "http://127.0.0.1:8000/api/books/?author=1&search=Harry&ordering=publication_year"
```

**Get a single book:**
```bash
curl http://127.0.0.1:8000/api/books/1/
```

**Create a book (requires authentication):**
```bash
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -d '{"title": "New Book", "publication_year": 2024, "author": 1}'
```

## Setup Instructions

1. Install dependencies:
```bash
   pip install django djangorestframework django-filter
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
│   ├── settings.py       # Project settings (includes django_filters)
│   └── urls.py           # Main URL configuration
├── api/
│   ├── models.py         # Author and Book models
│   ├── serializers.py    # BookSerializer and AuthorSerializer
│   ├── views.py          # Generic views with filtering, searching, ordering
│   └── urls.py           # API URL patterns
└── manage.py
```

## Implementation Details

### How Filtering Works
The `DjangoFilterBackend` allows exact matches on specified fields. Users can filter by passing field names as query parameters with their desired values.

### How Searching Works
The `SearchFilter` performs case-insensitive partial matching across specified fields. It uses Django's `icontains` lookup and can search across related fields using double-underscore notation (e.g., `author__name`).

### How Ordering Works
The `OrderingFilter` allows sorting results by any specified field. Ascending order is default, and descending order is achieved by prefixing the field name with a minus sign (`-`).