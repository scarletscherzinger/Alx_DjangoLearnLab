# Testing Documentation - Advanced API Project

## Overview
This document describes the testing strategy, test cases, and guidelines for running tests in the Advanced API Project.

## Testing Strategy

### Test Database Configuration
Django automatically creates a separate test database to avoid impacting production or development data:
- Test database is prefixed with `test_` (e.g., `test_db.sqlite3`)
- Created automatically before tests run
- Destroyed automatically after tests complete
- Completely isolated from development/production databases

### What We Test

#### 1. CRUD Operations
- **Create**: Test book creation with valid and invalid data
- **Read**: Test retrieving single books and lists of books
- **Update**: Test updating book information
- **Delete**: Test deleting books from the database

#### 2. Authentication & Permissions
- **Authenticated Access**: Verify authenticated users can create, update, and delete books
- **Unauthenticated Access**: Verify unauthenticated users are blocked from modification operations
- **Read-Only Access**: Verify unauthenticated users can view books

#### 3. Filtering
- **Filter by Title**: Test exact title matching
- **Filter by Author**: Test filtering by author ID
- **Filter by Publication Year**: Test filtering by year

#### 4. Searching
- **Search by Title**: Test searching across book titles
- **Search by Author**: Test searching across author names
- **Partial Matching**: Verify case-insensitive partial text matching

#### 5. Ordering
- **Ascending Order**: Test sorting by title and publication year (A-Z, oldest-newest)
- **Descending Order**: Test reverse sorting (-field)

#### 6. Validation
- **Future Publication Year**: Verify books with future years are rejected
- **Missing Required Fields**: Test validation for required fields

## Test Cases

### BookAPITestCase

| Test Method | Description | Expected Result |
|------------|-------------|-----------------|
| `test_list_books` | Get all books | 200 OK, returns all books |
| `test_retrieve_book` | Get single book by ID | 200 OK, returns correct book |
| `test_create_book_authenticated` | Create book (authenticated) | 201 Created, book saved |
| `test_create_book_unauthenticated` | Create book (no auth) | 403 Forbidden |
| `test_update_book_authenticated` | Update book (authenticated) | 200 OK, book updated |
| `test_update_book_unauthenticated` | Update book (no auth) | 403 Forbidden |
| `test_delete_book_authenticated` | Delete book (authenticated) | 204 No Content, book deleted |
| `test_delete_book_unauthenticated` | Delete book (no auth) | 403 Forbidden |
| `test_filter_books_by_title` | Filter by exact title | 200 OK, filtered results |
| `test_filter_books_by_author` | Filter by author ID | 200 OK, filtered results |
| `test_filter_books_by_publication_year` | Filter by year | 200 OK, filtered results |
| `test_search_books` | Search across fields | 200 OK, search results |
| `test_order_books_by_title` | Order by title (A-Z) | 200 OK, sorted results |
| `test_order_books_by_publication_year_descending` | Order by year (desc) | 200 OK, sorted results |
| `test_create_book_invalid_year` | Create with future year | 400 Bad Request |

## Running Tests

### Run All Tests
```bash
python manage.py test api
```

### Run Specific Test Class
```bash
python manage.py test api.test_views.BookAPITestCase
```

### Run Specific Test Method
```bash
python manage.py test api.test_views.BookAPITestCase.test_create_book_authenticated
```

### Run Tests with Verbose Output
```bash
python manage.py test api --verbosity=2
```

### Keep Test Database (for debugging)
```bash
python manage.py test api --keepdb
```

## Interpreting Test Results

### Successful Test Run
```
Ran 15 tests in 2.345s

OK
```
All tests passed successfully.

### Failed Test
```
FAIL: test_create_book_authenticated (api.test_views.BookAPITestCase)
AssertionError: 403 != 201
```
- Shows which test failed
- Shows the assertion that failed
- Indicates expected vs actual values

### Error in Test
```
ERROR: test_list_books (api.test_views.BookAPITestCase)
AttributeError: 'NoneType' object has no attribute 'id'
```
- Indicates a code error (not assertion failure)
- Shows the exception type and message

## Test Coverage

Our tests cover:
- ✅ All CRUD operations (Create, Read, Update, Delete)
- ✅ Authentication and permission enforcement
- ✅ Filtering by title, author, and publication year
- ✅ Searching across title and author fields
- ✅ Ordering by title and publication year
- ✅ Data validation (future publication years)
- ✅ Correct HTTP status codes for all scenarios

## Best Practices Followed

1. **Isolated Tests**: Each test is independent and doesn't rely on others
2. **Setup/Teardown**: Test data created in `setUp()` method
3. **Descriptive Names**: Test methods clearly describe what they test
4. **Documentation**: Each test has a docstring explaining purpose and expectations
5. **Status Code Verification**: All tests verify correct HTTP status codes
6. **Data Integrity**: Tests verify data changes in the database
7. **Separate Test Database**: Tests use isolated database to prevent data corruption

## Continuous Integration

These tests should be run:
- Before committing code changes
- As part of CI/CD pipeline
- Before deploying to production
- After any dependency updates

## Troubleshooting

### Test Database Issues
If you encounter database errors:
```bash
python manage.py test api --keepdb
```
This keeps the test database for inspection.

### Authentication Issues
Ensure test users are created in `setUp()` and properly authenticated in test methods.

### ImportError
Verify all imports in `test_views.py` are correct and models/views exist.