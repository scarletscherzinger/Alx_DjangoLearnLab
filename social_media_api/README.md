# Social Media API

## Project Overview
A Django REST Framework-based Social Media API with custom user authentication, token-based authorization, and user profile management.

## Features
- Custom User Model with bio, profile picture, and followers functionality
- Token-based authentication
- User registration with automatic token generation
- User login with token retrieval
- User profile management (view and update)

## Technology Stack
- Django 5.x
- Django REST Framework
- Token Authentication
- SQLite (development) / PostgreSQL (production)

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository:**
```bash
   git clone <repository-url>
   cd social_media_api
```

2. **Install dependencies:**
```bash
   pip install django djangorestframework
```

3. **Apply migrations:**
```bash
   python manage.py migrate
```

4. **Run the development server:**
```bash
   python manage.py runserver
```

## API Endpoints

### 1. User Registration
- **URL:** `/api/register/`
- **Method:** `POST`
- **Authentication:** None required
- **Request Body:**
```json
  {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "bio": "Software developer",
    "profile_picture": null
  }
```
- **Response (201 Created):**
```json
  {
    "user": {
      "username": "john_doe",
      "email": "john@example.com",
      "bio": "Software developer",
      "profile_picture": null
    },
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
  }
```

### 2. User Login
- **URL:** `/api/login/`
- **Method:** `POST`
- **Authentication:** None required
- **Request Body:**
```json
  {
    "username": "john_doe",
    "password": "securepassword123"
  }
```
- **Response (200 OK):**
```json
  {
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "bio": "Software developer",
      "profile_picture": null,
      "followers_count": 0,
      "following_count": 0
    }
  }
```

### 3. User Profile
- **URL:** `/api/profile/`
- **Method:** `GET`, `PUT`, `PATCH`
- **Authentication:** Token required
- **Headers:**
```
  Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```
- **Response (GET):**
```json
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "bio": "Software developer",
    "profile_picture": null,
    "followers_count": 0,
    "following_count": 0
  }
```

## Custom User Model

The `CustomUser` model extends Django's `AbstractUser` with additional fields:

- **bio** (TextField): User biography
- **profile_picture** (ImageField): Profile picture upload
- **followers** (ManyToManyField): Self-referential relationship for follower/following functionality

## Authentication

This API uses **Token Authentication**. After registration or login, include the token in the `Authorization` header:
```
Authorization: Token <your-token-here>
```

## Testing with Postman

1. **Register a new user:**
   - POST to `http://localhost:8000/api/register/`
   - Include username, email, password in request body
   - Save the returned token

2. **Login:**
   - POST to `http://localhost:8000/api/login/`
   - Include username and password
   - Save the returned token

3. **Access Profile:**
   - GET/PUT to `http://localhost:8000/api/profile/`
   - Add header: `Authorization: Token <your-token>`

## Project Structure
```
social_media_api/
├── accounts/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py          # CustomUser model
│   ├── serializers.py     # User serializers
│   ├── views.py           # API views
│   ├── urls.py            # Accounts URLs
│   └── tests.py
├── social_media_api/
│   ├── __init__.py
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py
├── manage.py
└── README.md
```

## Future Enhancements
- Post creation and management
- Comments and likes functionality
- Follow/unfollow users
- News feed based on followed users
- Profile picture upload handling
- Password reset functionality