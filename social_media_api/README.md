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

## Posts and Comments API

### Posts Endpoints

#### 1. List All Posts
- **URL:** `/api/posts/`
- **Method:** `GET`
- **Authentication:** Optional (public access)
- **Query Parameters:**
  - `page`: Page number (default: 1)
  - `page_size`: Results per page (default: 10, max: 100)
  - `search`: Search posts by title or content
- **Response (200 OK):**
```json
  {
    "count": 50,
    "next": "http://localhost:8000/api/posts/?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "author": "john_doe",
        "author_id": 1,
        "title": "My First Post",
        "content": "This is the content of my first post.",
        "created_at": "2025-12-13T10:30:00Z",
        "updated_at": "2025-12-13T10:30:00Z",
        "comments": [],
        "comments_count": 0
      }
    ]
  }
```

#### 2. Create a Post
- **URL:** `/api/posts/`
- **Method:** `POST`
- **Authentication:** Token required
- **Headers:** `Authorization: Token <your-token>`
- **Request Body:**
```json
  {
    "title": "My New Post",
    "content": "This is the content of my new post."
  }
```
- **Response (201 Created):**
```json
  {
    "id": 2,
    "author": "john_doe",
    "author_id": 1,
    "title": "My New Post",
    "content": "This is the content of my new post.",
    "created_at": "2025-12-13T11:00:00Z",
    "updated_at": "2025-12-13T11:00:00Z",
    "comments": [],
    "comments_count": 0
  }
```

#### 3. Retrieve a Post
- **URL:** `/api/posts/{id}/`
- **Method:** `GET`
- **Authentication:** Optional
- **Response (200 OK):** Same as create response with comments included

#### 4. Update a Post
- **URL:** `/api/posts/{id}/`
- **Method:** `PUT` or `PATCH`
- **Authentication:** Token required (must be author)
- **Headers:** `Authorization: Token <your-token>`
- **Request Body (PATCH):**
```json
  {
    "title": "Updated Title"
  }
```
- **Response (200 OK):** Updated post object

#### 5. Delete a Post
- **URL:** `/api/posts/{id}/`
- **Method:** `DELETE`
- **Authentication:** Token required (must be author)
- **Headers:** `Authorization: Token <your-token>`
- **Response (204 No Content)**

#### 6. Search Posts
- **URL:** `/api/posts/?search=keyword`
- **Method:** `GET`
- **Authentication:** Optional
- **Example:** `/api/posts/?search=django`
- **Response:** Paginated list of posts matching search in title or content

### Comments Endpoints

#### 1. List All Comments
- **URL:** `/api/comments/`
- **Method:** `GET`
- **Authentication:** Optional
- **Query Parameters:**
  - `page`: Page number
  - `page_size`: Results per page
- **Response (200 OK):**
```json
  {
    "count": 25,
    "next": "http://localhost:8000/api/comments/?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "post": 1,
        "author": "jane_smith",
        "author_id": 2,
        "content": "Great post!",
        "created_at": "2025-12-13T10:45:00Z",
        "updated_at": "2025-12-13T10:45:00Z"
      }
    ]
  }
```

#### 2. Create a Comment
- **URL:** `/api/comments/`
- **Method:** `POST`
- **Authentication:** Token required
- **Headers:** `Authorization: Token <your-token>`
- **Request Body:**
```json
  {
    "post": 1,
    "content": "This is my comment on the post."
  }
```
- **Response (201 Created):**
```json
  {
    "id": 2,
    "post": 1,
    "author": "john_doe",
    "author_id": 1,
    "content": "This is my comment on the post.",
    "created_at": "2025-12-13T11:15:00Z",
    "updated_at": "2025-12-13T11:15:00Z"
  }
```

#### 3. Retrieve a Comment
- **URL:** `/api/comments/{id}/`
- **Method:** `GET`
- **Authentication:** Optional
- **Response (200 OK):** Comment object

#### 4. Update a Comment
- **URL:** `/api/comments/{id}/`
- **Method:** `PUT` or `PATCH`
- **Authentication:** Token required (must be author)
- **Headers:** `Authorization: Token <your-token>`
- **Request Body:**
```json
  {
    "content": "Updated comment content"
  }
```
- **Response (200 OK):** Updated comment object

#### 5. Delete a Comment
- **URL:** `/api/comments/{id}/`
- **Method:** `DELETE`
- **Authentication:** Token required (must be author)
- **Headers:** `Authorization: Token <your-token>`
- **Response (204 No Content)**

## Permissions

### Posts and Comments
- **Read (GET):** Anyone (authenticated or not)
- **Create (POST):** Authenticated users only
- **Update (PUT/PATCH):** Author only
- **Delete (DELETE):** Author only

The custom `IsAuthorOrReadOnly` permission ensures that:
- Anyone can view posts and comments
- Only authenticated users can create posts and comments
- Only the author can edit or delete their own posts and comments

## Features

### Pagination
- Default page size: 10 items
- Customizable via `page_size` query parameter (max: 100)
- Provides `next` and `previous` links for navigation

### Filtering and Search
- **Posts:** Search by title or content using `?search=keyword`
- Returns results matching the keyword in either field

### Data Validation
- All fields are validated by serializers
- Foreign keys ensure data integrity
- Timestamps are automatically managed

## User Follow System and Feed

### Follow Management Endpoints

#### 1. Follow a User
- **URL:** `/follow/<int:user_id>/`
- **Method:** `POST`
- **Authentication:** Token required
- **Headers:** `Authorization: Token <your-token>`
- **Response (200 OK):**
```json
  {
    "message": "You are now following username"
  }
```
- **Error Responses:**
  - 400: "You cannot follow yourself"
  - 404: "User not found"

#### 2. Unfollow a User
- **URL:** `/unfollow/<int:user_id>/`
- **Method:** `POST`
- **Authentication:** Token required
- **Headers:** `Authorization: Token <your-token>`
- **Response (200 OK):**
```json
  {
    "message": "You have unfollowed username"
  }
```
- **Error Response:**
  - 404: "User not found"

### Feed Endpoint

#### View Feed from Followed Users
- **URL:** `/api/feed/`
- **Method:** `GET`
- **Authentication:** Token required
- **Headers:** `Authorization: Token <your-token>`
- **Query Parameters:**
  - `page`: Page number (default: 1)
  - `page_size`: Results per page (default: 10, max: 100)
- **Response (200 OK):**
```json
  {
    "count": 25,
    "next": "http://localhost:8000/api/feed/?page=2",
    "previous": null,
    "results": [
      {
        "id": 5,
        "author": "followed_user",
        "author_id": 3,
        "title": "Post from followed user",
        "content": "This post appears in your feed",
        "created_at": "2025-12-13T12:00:00Z",
        "updated_at": "2025-12-13T12:00:00Z",
        "comments": [],
        "comments_count": 0
      }
    ]
  }
```

## User Relationships

The CustomUser model includes a **followers/following** system:

- **followers**: ManyToManyField representing users who follow this user
- **following** (reverse relationship): Users that this user follows

### How It Works:
1. User A follows User B: `user_a.following.add(user_b)`
2. User B's followers include User A: `user_b.followers.all()` contains User A
3. Feed shows posts from users in `user.following.all()`

## Usage Examples

### Example 1: Follow a User
```bash
POST /follow/5/
Headers: Authorization: Token abc123...

Response:
{
  "message": "You are now following jane_doe"
}
```

### Example 2: View Your Feed
```bash
GET /api/feed/
Headers: Authorization: Token abc123...

Returns: Posts from all users you follow, most recent first
```

### Example 3: Unfollow a User
```bash
POST /unfollow/5/
Headers: Authorization: Token abc123...

Response:
{
  "message": "You have unfollowed jane_doe"
}
```
## Likes and Notifications System

### Like Endpoints

#### 1. Like a Post
- **URL:** `/api/posts/<int:pk>/like/`
- **Method:** `POST`
- **Authentication:** Token required
- **Headers:** `Authorization: Token <your-token>`
- **Response (201 Created):**
```json
  {
    "message": "Post liked successfully"
  }
```
- **Error Responses:**
  - 400: "You already liked this post"
  - 404: "Post not found"

#### 2. Unlike a Post
- **URL:** `/api/posts/<int:pk>/unlike/`
- **Method:** `POST`
- **Authentication:** Token required
- **Headers:** `Authorization: Token <your-token>`
- **Response (200 OK):**
```json
  {
    "message": "Post unliked successfully"
  }
```
- **Error Responses:**
  - 400: "You have not liked this post"
  - 404: "Post not found"

### Notification Endpoints

#### 1. View All Notifications
- **URL:** `/notifications/`
- **Method:** `GET`
- **Authentication:** Token required
- **Headers:** `Authorization: Token <your-token>`
- **Response (200 OK):**
```json
  [
    {
      "id": 1,
      "recipient": 1,
      "actor": "john_doe",
      "verb": "liked your post",
      "target_content_type": 10,
      "target_object_id": 5,
      "timestamp": "2025-12-13T12:30:00Z",
      "read": false
    },
    {
      "id": 2,
      "recipient": 1,
      "actor": "jane_smith",
      "verb": "started following you",
      "target_content_type": null,
      "target_object_id": null,
      "timestamp": "2025-12-13T11:00:00Z",
      "read": true
    }
  ]
```

#### 2. Mark Notification as Read
- **URL:** `/notifications/<int:pk>/read/`
- **Method:** `POST`
- **Authentication:** Token required
- **Headers:** `Authorization: Token <your-token>`
- **Response (200 OK):**
```json
  {
    "message": "Notification marked as read"
  }
```
- **Error Response:**
  - 404: "Notification not found"

## Notification System

### How It Works
Notifications are automatically generated for the following actions:

1. **Post Liked**: When someone likes your post
   - Recipient: Post author
   - Actor: User who liked
   - Verb: "liked your post"
   - Target: The post object

2. **New Follower**: When someone follows you (to be implemented)
   - Recipient: User being followed
   - Actor: User who followed
   - Verb: "started following you"

3. **New Comment**: When someone comments on your post (to be implemented)
   - Recipient: Post author
   - Actor: User who commented
   - Verb: "commented on your post"
   - Target: The comment object

### Notification Fields
- **recipient**: User receiving the notification
- **actor**: User performing the action
- **verb**: Description of the action (e.g., "liked your post")
- **target**: GenericForeignKey to the related object (post, comment, etc.)
- **timestamp**: When the notification was created
- **read**: Boolean indicating if notification has been read

### Like System

#### Like Model
- Tracks which users liked which posts
- Prevents duplicate likes (unique constraint on user + post)
- Automatically creates notification for post author

## Usage Examples

### Example 1: Like a Post
```bash
POST /api/posts/5/like/
Headers: Authorization: Token abc123...

Response:
{
  "message": "Post liked successfully"
}
```

### Example 2: View Your Notifications
```bash
GET /notifications/
Headers: Authorization: Token abc123...

Returns: List of all notifications for the authenticated user
```

### Example 3: Mark Notification as Read
```bash
POST /notifications/3/read/
Headers: Authorization: Token abc123...

Response:
{
  "message": "Notification marked as read"
}
```

## Future Enhancements
- Post creation and management
- Comments and likes functionality
- Follow/unfollow users
- News feed based on followed users
- Profile picture upload handling
- Password reset functionality