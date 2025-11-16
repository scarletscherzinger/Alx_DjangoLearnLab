# Permissions and Groups Setup

## Custom Permissions

This application uses Django's permission system to control access to Book operations.

### Book Model Permissions

The `Book` model in `bookshelf/models.py` defines four custom permissions:

- `can_view` - Allows viewing books
- `can_create` - Allows creating new books
- `can_edit` - Allows editing existing books
- `can_delete` - Allows deleting books

## Groups and Permission Assignment

Three user groups have been created with specific permissions:

### 1. Viewers
- Permissions: `can_view`
- Can only view the list of books

### 2. Editors
- Permissions: `can_view`, `can_create`, `can_edit`
- Can view, create, and edit books but cannot delete them

### 3. Admins
- Permissions: `can_view`, `can_create`, `can_edit`, `can_delete`
- Full access to all book operations

## Permission Enforcement in Views

Views in `bookshelf/views.py` use the `@permission_required` decorator to enforce permissions:

- `book_list` - Requires `bookshelf.can_view`
- `book_create` - Requires `bookshelf.can_create`
- `book_edit` - Requires `bookshelf.can_edit`
- `book_delete` - Requires `bookshelf.can_delete`

## Setting Up Groups (via Django Admin)

1. Create a superuser: `python manage.py createsuperuser`
2. Run the server: `python manage.py runserver`
3. Access admin at: `http://127.0.0.1:8000/admin/`
4. Navigate to "Groups" and create: Viewers, Editors, Admins
5. Assign the appropriate permissions to each group
6. Add users to groups as needed

## Testing Permissions

1. Create test users via Django admin
2. Assign users to different groups
3. Log in as each user and verify access levels
4. Users without proper permissions will see a 403 Forbidden error