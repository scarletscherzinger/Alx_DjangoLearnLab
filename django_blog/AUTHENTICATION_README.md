# Django Blog Authentication System Documentation

## Overview
This Django blog project implements a comprehensive user authentication system that allows users to register, login, logout, and manage their profiles.

## Authentication Features

### 1. User Registration
- **URL**: `/register/`
- **Template**: `blog/templates/blog/register.html`
- **View**: `blog.views.register`
- **Form**: `CustomUserCreationForm` (extends Django's `UserCreationForm`)

**How it works:**
- Users can create a new account by providing a username, email, and password
- The form includes built-in validation for password strength and username uniqueness
- Email field is required (custom addition to Django's default UserCreationForm)
- Upon successful registration, users are automatically logged in and redirected to their profile page
- CSRF protection is enabled on the registration form

**Testing Registration:**
1. Navigate to `http://127.0.0.1:8000/register/`
2. Fill in username, email, password, and password confirmation
3. Submit the form
4. Verify you're redirected to the profile page and logged in

### 2. User Login
- **URL**: `/login/`
- **Template**: `blog/templates/blog/login.html`
- **View**: Django's built-in `LoginView`

**How it works:**
- Users log in with their username and password
- Django's built-in authentication backend validates credentials
- Passwords are securely hashed using Django's default PBKDF2 algorithm
- After successful login, users are redirected to their profile page (configured via `LOGIN_REDIRECT_URL`)
- Failed login attempts display error messages
- CSRF protection is enabled on the login form

**Testing Login:**
1. Navigate to `http://127.0.0.1:8000/login/`
2. Enter your username and password
3. Submit the form
4. Verify you're redirected to the profile page

### 3. User Logout
- **URL**: `/logout/`
- **Template**: `blog/templates/blog/logout.html`
- **View**: Django's built-in `LogoutView`

**How it works:**
- Users can log out by clicking the logout link in the navigation
- Django terminates the user's session
- Users are redirected to the logout confirmation page
- From there, they can log in again

**Testing Logout:**
1. While logged in, click the "Logout" link in navigation
2. Verify you're redirected to the logout confirmation page
3. Verify navigation now shows "Login" and "Register" instead of "Profile" and "Logout"

### 4. Profile Management
- **URL**: `/profile/`
- **Template**: `blog/templates/blog/profile.html`
- **View**: `blog.views.profile`
- **Decorator**: `@login_required`

**How it works:**
- Only authenticated users can access this page (enforced by `@login_required` decorator)
- Users can view their current username and email
- Users can update their email address via POST request
- Username is displayed but cannot be changed (disabled input field)
- CSRF protection is enabled on the profile form
- After updating, users remain on the profile page with updated information

**Testing Profile:**
1. Log in to your account
2. Navigate to `http://127.0.0.1:8000/profile/` or click "Profile" in navigation
3. Verify your username and email are displayed
4. Change your email address and submit
5. Verify the email is updated and you remain on the profile page

## Security Features

### 1. CSRF Protection
All forms include `{% csrf_token %}` to prevent Cross-Site Request Forgery attacks:
- Registration form
- Login form
- Profile update form

### 2. Password Security
- Passwords are hashed using Django's default PBKDF2 algorithm with SHA256
- Passwords are never stored in plain text
- Password strength validation is enforced (minimum 8 characters, can't be too common, etc.)

### 3. Login Required Decorator
The profile view uses `@login_required` decorator to ensure only authenticated users can access it. Unauthenticated users are redirected to the login page.

### 4. Session Management
Django's session framework manages user authentication state securely with server-side session storage.

## File Structure
```
django_blog/
├── blog/
│   ├── forms.py              # CustomUserCreationForm
│   ├── views.py              # register, profile views
│   ├── urls.py               # URL routing for authentication
│   ├── templates/
│   │   └── blog/
│   │       ├── base.html     # Base template with dynamic navigation
│   │       ├── login.html    # Login page
│   │       ├── register.html # Registration page
│   │       ├── logout.html   # Logout confirmation
│   │       ├── profile.html  # Profile management
│   │       ├── home.html     # Home page
│   │       └── posts.html    # Blog posts page
│   └── static/
│       ├── css/
│       │   └── styles.css    # Styling for all pages
│       └── js/
│           └── scripts.js    # JavaScript functionality
└── django_blog/
    ├── settings.py           # LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL configured
    └── urls.py               # Includes blog URLs
```

## Configuration Settings

In `django_blog/settings.py`:
```python
# Redirect URLs after login/logout
LOGIN_REDIRECT_URL = 'profile'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'
```

## Custom Forms

### CustomUserCreationForm
Located in `blog/forms.py`, this form extends Django's `UserCreationForm` to include:
- Email field (required)
- Custom save method to store email address

## Testing Instructions

### Complete Testing Workflow

1. **Start the development server:**
```bash
   python manage.py runserver
```

2. **Test Registration:**
   - Go to `http://127.0.0.1:8000/register/`
   - Create a new account with username, email, and password
   - Verify automatic login and redirect to profile

3. **Test Profile Management:**
   - On profile page, update your email
   - Submit the form
   - Verify email is updated

4. **Test Logout:**
   - Click "Logout" in navigation
   - Verify redirect to logout page
   - Verify navigation changes to show Login/Register

5. **Test Login:**
   - Click "Login" link
   - Enter credentials
   - Verify redirect to profile page

6. **Test Login Required:**
   - While logged out, try to access `http://127.0.0.1:8000/profile/`
   - Verify you're redirected to login page

7. **Test Invalid Credentials:**
   - Try logging in with wrong password
   - Verify error message is displayed

8. **Test Dynamic Navigation:**
   - While logged out, verify navigation shows "Login" and "Register"
   - While logged in, verify navigation shows "Profile" and "Logout"

## User Interaction Flow

1. **New User Journey:**
   - User visits homepage
   - Clicks "Register" in navigation
   - Fills out registration form
   - Automatically logged in and redirected to profile
   - Can now access all authenticated features

2. **Returning User Journey:**
   - User visits homepage
   - Clicks "Login" in navigation
   - Enters credentials
   - Redirected to profile page
   - Can update profile information
   - Can logout when done

## Technical Details

### Authentication Backend
Django's default authentication backend (`django.contrib.auth.backends.ModelBackend`) is used, which:
- Authenticates against `django.contrib.auth.models.User`
- Uses username and password for authentication
- Supports permission and group checking

### Password Hashing
Django uses PBKDF2 algorithm with SHA256 hash by default:
- 260,000 iterations (as of Django 4.2)
- Highly resistant to brute-force attacks
- Automatically upgraded if Django improves the algorithm

### Session Security
- Sessions are stored server-side
- Session cookies are HttpOnly by default (prevents XSS attacks)
- Session data expires after browser closes or configured timeout

## Troubleshooting

**Problem**: Can't access profile page
**Solution**: Make sure you're logged in. The profile view requires authentication.

**Problem**: Registration form shows validation errors
**Solution**: Ensure passwords match, meet strength requirements (8+ characters, not too common), and username is unique.

**Problem**: Static files not loading
**Solution**: Ensure `{% load static %}` is at the top of base.html and `STATIC_URL` is configured in settings.py.

**Problem**: CSRF token missing or incorrect
**Solution**: Ensure `{% csrf_token %}` is inside all `<form>` tags and Django's CSRF middleware is enabled.

## Future Enhancements

Potential improvements to the authentication system:
- Email verification during registration
- Password reset functionality via email
- Profile picture upload
- Extended user profile with bio, location, etc.
- Social authentication (Google, GitHub, etc.)
- Two-factor authentication (2FA)
- Remember me functionality
- Account deletion option