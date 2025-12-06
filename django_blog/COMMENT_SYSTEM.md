# Comment System Documentation

## Overview
This Django blog project implements a comprehensive comment system that allows users to interact with blog posts through comments. Authenticated users can create, edit, and delete their own comments, while all visitors can view comments on posts.

## Comment Model

### Model Structure
The `Comment` model is defined in `blog/models.py` with the following fields:
```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Field Descriptions
- **post**: Foreign key linking to the Post model (many-to-one relationship)
- **author**: Foreign key linking to Django's User model
- **content**: TextField for the comment text
- **created_at**: Timestamp of when comment was created (auto-set)
- **updated_at**: Timestamp of when comment was last modified (auto-updated)

### Model Features
- Comments are ordered by newest first (`ordering = ['-created_at']`)
- Related name 'comments' allows access via `post.comments.all()`
- Cascade deletion: if a post or user is deleted, their comments are also deleted

---

## Comment Features

### 1. View Comments
- **Access**: Public (all users)
- **Location**: Displayed on post detail page
- **URL**: `/post/<int:pk>/` (part of post detail)

**Features:**
- Shows all comments for a specific post
- Displays comment author, content, and timestamp
- Shows "(edited)" indicator if comment was modified
- Shows comment count
- Orders comments by newest first

**Testing:**
1. Navigate to any blog post detail page
2. Scroll to the comments section
3. Verify all comments are displayed with proper information

---

### 2. Add Comment
- **Access**: Authenticated users only
- **URL**: `/post/<int:post_id>/comments/new/`
- **View**: `add_comment` (function-based view)
- **Template**: `blog/add_comment.html`
- **Form**: `CommentForm`

**Features:**
- Allows authenticated users to post comments on blog posts
- Form validates that content is at least 3 characters long
- Automatically sets the comment author to the logged-in user
- Automatically links comment to the specific post
- Redirects to post detail page after successful comment creation
- Unauthenticated users see "Login to comment" link

**Testing:**
1. Log in to your account
2. Navigate to a blog post
3. Click "Add Comment"
4. Write a comment (at least 3 characters)
5. Submit the form
6. Verify you're redirected to the post and your comment appears

**Testing Login Required:**
1. Log out
2. Navigate to a post detail page
3. Verify you see "Login to comment" instead of "Add Comment"

---

### 3. Edit Comment
- **Access**: Comment author only
- **URL**: `/comment/<int:pk>/update/`
- **View**: `CommentUpdateView` (class-based view)
- **Template**: `blog/edit_comment.html`
- **Mixins**: LoginRequiredMixin, UserPassesTestMixin

**Features:**
- Allows only the comment author to edit their comments
- Pre-fills form with existing comment content
- Updates the `updated_at` timestamp automatically
- Shows "(edited)" indicator on the comment after update
- Validates that content is at least 3 characters long
- Returns 403 Forbidden if non-author tries to edit
- Redirects to post detail page after successful update

**Testing:**
1. Log in as the comment author
2. View a post where you have comments
3. Click "Edit" on your comment
4. Modify the content
5. Submit the form
6. Verify changes are saved and "(edited)" appears

**Testing Author-Only Access:**
1. Log in as a different user
2. Try to access `/comment/<pk>/update/` for someone else's comment
3. Verify you get a 403 Forbidden error

---

### 4. Delete Comment
- **Access**: Comment author only
- **URL**: `/comment/<int:pk>/delete/`
- **View**: `CommentDeleteView` (class-based view)
- **Template**: `blog/delete_comment.html`
- **Mixins**: LoginRequiredMixin, UserPassesTestMixin

**Features:**
- Allows only the comment author to delete their comments
- Shows confirmation page before deletion
- Displays the comment content on confirmation page
- Validates that only the author can delete (UserPassesTestMixin)
- Returns 403 Forbidden if non-author tries to delete
- Redirects to post detail page after successful deletion

**Testing:**
1. Log in as the comment author
2. View a post where you have comments
3. Click "Delete" on your comment
4. Verify confirmation page appears with comment text
5. Click "Yes, Delete"
6. Verify comment is removed and you're redirected to the post

**Testing Author-Only Access:**
1. Log in as a different user
2. Try to access `/comment/<pk>/delete/` for someone else's comment
3. Verify you get a 403 Forbidden error

---

## CommentForm

### Form Definition
Located in `blog/forms.py`:
```python
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your comment here...'
            })
        }
```

### Validation Rules
- **Content**: Required field
- **Minimum length**: 3 characters
- **Clean method**: Custom validation to ensure quality comments
```python
def clean_content(self):
    content = self.cleaned_data.get('content')
    if not content or len(content.strip()) < 3:
        raise forms.ValidationError('Comment must be at least 3 characters long.')
    return content
```

---

## URL Patterns

### Comment URLs
```python
path('post/<int:post_id>/comments/new/', views.add_comment, name='add-comment'),
path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='edit-comment'),
path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete-comment'),
```

### URL Structure Logic
- **Create**: Uses `post_id` to associate comment with specific post
- **Update/Delete**: Uses comment `pk` (primary key) to identify specific comment
- **Intuitive paths**: Clear indication of action and resource

---

## Permissions and Access Control

### Public Access (No Authentication Required)
- **View comments** - Anyone can see comments on posts

### Authenticated Users Only
- **Create comment** - Must be logged in to comment

### Author-Only Access
- **Edit comment** - Only comment author (LoginRequiredMixin + UserPassesTestMixin)
- **Delete comment** - Only comment author (LoginRequiredMixin + UserPassesTestMixin)

### How UserPassesTestMixin Works
The `test_func()` method verifies the user is the comment author:
```python
def test_func(self):
    comment = self.get_object()
    return self.request.user == comment.author
```

- Returns `True` if user is the author (access granted)
- Returns `False` if user is not the author (403 Forbidden)

---

## Template Integration

### post_detail.html Updates
The post detail template now includes:

1. **Comment count display**
```html
   <h2>Comments ({{ post.comments.count }})</h2>
```

2. **Add comment link** (authenticated users only)
```html
   {% if user.is_authenticated %}
       <a href="{% url 'add-comment' post.pk %}">Add Comment</a>
   {% endif %}
```

3. **Comments list**
```html
   {% for comment in post.comments.all %}
       <!-- Comment display with edit/delete for author -->
   {% endfor %}
```

4. **Edit indicator**
```html
   {% if comment.created_at != comment.updated_at %}
       (edited)
   {% endif %}
```

5. **Author-only actions**
```html
   {% if user == comment.author %}
       <a href="{% url 'edit-comment' comment.pk %}">Edit</a>
       <a href="{% url 'delete-comment' comment.pk %}">Delete</a>
   {% endif %}
```

---

## Security Features

### 1. CSRF Protection
All forms include `{% csrf_token %}` to prevent Cross-Site Request Forgery attacks:
- Add comment form
- Edit comment form
- Delete comment confirmation

### 2. Login Required
- `add_comment` view uses `@login_required` decorator
- `CommentUpdateView` uses `LoginRequiredMixin`
- `CommentDeleteView` uses `LoginRequiredMixin`

### 3. Author-Only Access
- `CommentUpdateView` uses `UserPassesTestMixin` with `test_func()`
- `CommentDeleteView` uses `UserPassesTestMixin` with `test_func()`
- Non-authors receive 403 Forbidden error

### 4. Automatic Author Assignment
When creating a comment, the author is automatically set:
```python
comment.author = request.user
```

### 5. Automatic Post Association
Comments are automatically linked to the correct post:
```python
comment.post = post
```

---

## Data Flow

### Creating a Comment
1. User clicks "Add Comment" on post detail page
2. User is redirected to `/post/<post_id>/comments/new/`
3. User fills out comment form
4. Form validates content (min 3 characters)
5. View sets `author` and `post` automatically
6. Comment is saved to database
7. User is redirected back to post detail page
8. New comment appears in the comments section

### Editing a Comment
1. Comment author clicks "Edit" on their comment
2. User is redirected to `/comment/<pk>/update/`
3. Form is pre-filled with existing comment content
4. User modifies the content
5. Form validates content
6. `updated_at` timestamp is automatically updated
7. Comment is saved
8. User is redirected back to post detail page
9. Comment shows "(edited)" indicator

### Deleting a Comment
1. Comment author clicks "Delete" on their comment
2. User is redirected to `/comment/<pk>/delete/`
3. Confirmation page shows the comment content
4. User confirms deletion
5. Comment is removed from database
6. User is redirected back to post detail page
7. Comment no longer appears

---

## Complete Testing Workflow

### 1. Create Test Users and Posts
```bash
python manage.py createsuperuser
python manage.py shell
>>> from blog.models import Post
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='youruser')
>>> Post.objects.create(title='Test Post', content='Content', author=user)
```

### 2. Test Comment Viewing (Public)
1. Log out (if logged in)
2. Navigate to a post detail page
3. Verify you can see existing comments
4. Verify you see "Login to comment" link

### 3. Test Comment Creation
1. Log in as User A
2. Navigate to a post
3. Click "Add Comment"
4. Write a comment
5. Submit the form
6. Verify comment appears on the post

### 4. Test Comment Editing
1. While logged in as User A (comment author)
2. Click "Edit" on your comment
3. Modify the content
4. Submit the form
5. Verify changes are saved
6. Verify "(edited)" indicator appears

### 5. Test Comment Deletion
1. While logged in as User A (comment author)
2. Click "Delete" on your comment
3. Verify confirmation page appears
4. Click "Yes, Delete"
5. Verify comment is removed

### 6. Test Author-Only Permissions
1. Log in as User B (not the comment author)
2. Try to access edit URL for User A's comment directly
3. Verify you get 403 Forbidden
4. Try to access delete URL for User A's comment directly
5. Verify you get 403 Forbidden
6. Verify you don't see Edit/Delete links on User A's comments

### 7. Test Form Validation
1. Try to submit an empty comment
2. Verify you get a validation error
3. Try to submit a comment with only 1-2 characters
4. Verify you get "Comment must be at least 3 characters long" error

---

## File Structure
```
django_blog/
├── blog/
│   ├── models.py              # Comment model
│   ├── forms.py               # CommentForm
│   ├── views.py               # Comment CRUD views
│   ├── urls.py                # Comment URL patterns
│   ├── migrations/
│   │   └── 0002_comment.py    # Comment model migration
│   └── templates/
│       └── blog/
│           ├── post_detail.html         # Updated with comments section
│           ├── add_comment.html         # Create comment
│           ├── edit_comment.html        # Update comment
│           └── delete_comment.html      # Delete comment
└── COMMENT_SYSTEM.md          # This documentation
```

---

## Database Schema

### Comment Table
```
comments
├── id (PK)
├── post_id (FK → posts.id)
├── author_id (FK → auth_user.id)
├── content (TextField)
├── created_at (DateTime)
└── updated_at (DateTime)
```

### Relationships
- One Post → Many Comments (one-to-many)
- One User → Many Comments (one-to-many)

---

## Troubleshooting

**Problem**: Can't add comments
**Solution**: Make sure you're logged in. Only authenticated users can create comments.

**Problem**: Can't edit someone else's comment
**Solution**: This is intentional. Only the comment author can edit their comments.

**Problem**: Getting 403 Forbidden when trying to edit/delete
**Solution**: You're not the author of that comment. Only authors can edit/delete their own comments.

**Problem**: "(edited)" indicator not showing
**Solution**: The comment hasn't been edited yet, or `created_at` and `updated_at` are the same.

**Problem**: Comments not appearing on post
**Solution**: Make sure comments exist in the database. Check in Django admin or create test comments.

---

## Future Enhancements

Potential improvements:
- Add reply functionality (nested comments)
- Implement comment voting/likes
- Add comment moderation for admins
- Include comment reporting system
- Add pagination for comments
- Implement real-time comments with WebSockets
- Add rich text formatting for comments
- Include comment notifications
- Add comment search functionality