# Blog Post Management Features Documentation

## Overview
This Django blog project implements complete CRUD (Create, Read, Update, Delete) operations for blog posts using Django's class-based views. The system allows authenticated users to create posts and manage their own content while allowing all visitors to view posts.

## Features

### 1. List All Blog Posts (ListView)
- **URL**: `/posts/`
- **View**: `PostListView`
- **Template**: `blog/post_list.html`
- **Access**: Public (all users)

**Features:**
- Displays all blog posts ordered by published date (newest first)
- Shows post title, author, publication date, and content snippet (first 30 words)
- Provides "Read More" link to view full post
- Shows "Create New Post" button for authenticated users
- Accessible to both authenticated and anonymous users

**Testing:**
1. Navigate to `http://127.0.0.1:8000/posts/`
2. Verify all posts are displayed
3. Check that posts are ordered by newest first
4. Verify "Create New Post" link appears only when logged in

---

### 2. View Individual Blog Post (DetailView)
- **URL**: `/posts/<int:pk>/`
- **View**: `PostDetailView`
- **Template**: `blog/post_detail.html`
- **Access**: Public (all users)

**Features:**
- Displays complete blog post content
- Shows post title, author, publication date
- Displays full content with proper line breaks
- Shows "Edit Post" and "Delete Post" links only to the post author
- Provides "Back to All Posts" link

**Testing:**
1. Click on any post from the post list
2. Verify full content is displayed
3. If you're the author, verify edit/delete links appear
4. If you're not the author, verify edit/delete links do NOT appear

---

### 3. Create New Blog Post (CreateView)
- **URL**: `/posts/new/`
- **View**: `PostCreateView`
- **Template**: `blog/post_form.html`
- **Access**: Authenticated users only (LoginRequiredMixin)

**Features:**
- Allows authenticated users to create new blog posts
- Form includes fields for title and content
- Automatically sets the author to the logged-in user
- Validates that title and content are not empty
- Redirects to the newly created post detail page after successful creation
- Unauthenticated users are redirected to login page

**Testing:**
1. Log in to your account
2. Navigate to `http://127.0.0.1:8000/posts/new/` or click "Create New Post"
3. Fill in title and content
4. Submit the form
5. Verify you're redirected to the new post's detail page
6. Verify the post appears in the post list

**Testing Login Required:**
1. Log out
2. Try to access `http://127.0.0.1:8000/posts/new/`
3. Verify you're redirected to the login page

---

### 4. Edit Existing Blog Post (UpdateView)
- **URL**: `/posts/<int:pk>/edit/`
- **View**: `PostUpdateView`
- **Template**: `blog/post_form.html`
- **Access**: Post author only (LoginRequiredMixin + UserPassesTestMixin)

**Features:**
- Allows only the post author to edit their posts
- Pre-fills form with existing post data
- Form includes fields for title and content
- Validates that only the author can edit (UserPassesTestMixin)
- Redirects to the updated post detail page after successful edit
- Returns 403 Forbidden if non-author tries to edit

**Testing:**
1. Log in as the post author
2. View one of your posts
3. Click "Edit Post"
4. Modify the title or content
5. Submit the form
6. Verify changes are saved and you're redirected to the post detail page

**Testing Author-Only Access:**
1. Log in as a different user (not the post author)
2. Try to access `/posts/<pk>/edit/` for someone else's post
3. Verify you get a 403 Forbidden error or are redirected

---

### 5. Delete Blog Post (DeleteView)
- **URL**: `/posts/<int:pk>/delete/`
- **View**: `PostDeleteView`
- **Template**: `blog/post_confirm_delete.html`
- **Access**: Post author only (LoginRequiredMixin + UserPassesTestMixin)

**Features:**
- Allows only the post author to delete their posts
- Shows confirmation page before deletion
- Validates that only the author can delete (UserPassesTestMixin)
- Redirects to post list page after successful deletion
- Returns 403 Forbidden if non-author tries to delete

**Testing:**
1. Log in as the post author
2. View one of your posts
3. Click "Delete Post"
4. Verify confirmation page appears
5. Click "Yes, Delete"
6. Verify post is deleted and you're redirected to post list
7. Verify post no longer appears in the list

**Testing Author-Only Access:**
1. Log in as a different user (not the post author)
2. Try to access `/posts/<pk>/delete/` for someone else's post
3. Verify you get a 403 Forbidden error or are redirected

---

## Class-Based Views Used

### ListView (PostListView)
```python
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
```
- Displays all posts
- Orders by published date (newest first)
- Public access

### DetailView (PostDetailView)
```python
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
```
- Shows individual post
- Public access

### CreateView (PostCreateView)
```python
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
```
- Requires authentication (LoginRequiredMixin)
- Automatically sets author to logged-in user
- Redirects to post detail after creation

### UpdateView (PostUpdateView)
```python
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
```
- Requires authentication (LoginRequiredMixin)
- Checks if user is the author (UserPassesTestMixin)
- Returns 403 if test_func returns False

### DeleteView (PostDeleteView)
```python
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
```
- Requires authentication (LoginRequiredMixin)
- Checks if user is the author (UserPassesTestMixin)
- Shows confirmation before deletion

---

## Permissions and Access Control

### Public Access (No Authentication Required)
- **List all posts** (`/posts/`)
- **View individual post** (`/posts/<pk>/`)

### Authenticated Users Only
- **Create new post** (`/posts/new/`) - LoginRequiredMixin

### Author-Only Access
- **Edit post** (`/posts/<pk>/edit/`) - LoginRequiredMixin + UserPassesTestMixin
- **Delete post** (`/posts/<pk>/delete/`) - LoginRequiredMixin + UserPassesTestMixin

**How UserPassesTestMixin Works:**
The `test_func()` method checks if the current user is the author:
```python
def test_func(self):
    post = self.get_object()
    return self.request.user == post.author
```
- Returns `True` if user is the author (access granted)
- Returns `False` if user is not the author (403 Forbidden)

---

## URL Patterns
```python
urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/new/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-edit'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
]
```

---

## Templates

### post_list.html
- Lists all blog posts
- Shows title, author, date, and content snippet
- Provides links to read full posts
- Shows "Create New Post" button for authenticated users

### post_detail.html
- Displays full blog post
- Shows edit/delete links only to post author
- Provides navigation back to post list

### post_form.html
- Shared template for create and edit operations
- Uses `{% csrf_token %}` for security
- Shows different title based on create vs. edit
- Pre-fills data when editing

### post_confirm_delete.html
- Confirms deletion before removing post
- Uses `{% csrf_token %}` for security
- Provides cancel option

---

## Security Features

### 1. CSRF Protection
All forms include `{% csrf_token %}` to prevent Cross-Site Request Forgery attacks.

### 2. Login Required
- CreateView uses `LoginRequiredMixin`
- UpdateView uses `LoginRequiredMixin`
- DeleteView uses `LoginRequiredMixin`
- Unauthenticated users are redirected to login page

### 3. Author-Only Access
- UpdateView uses `UserPassesTestMixin` with `test_func()`
- DeleteView uses `UserPassesTestMixin` with `test_func()`
- Non-authors receive 403 Forbidden error

### 4. Automatic Author Assignment
When creating a post, the author is automatically set to the logged-in user:
```python
def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)
```

---

## Data Validation

### Form Fields
- **Title**: Required, max 200 characters
- **Content**: Required, unlimited text
- **Author**: Automatically set, not editable by user
- **Published Date**: Automatically set on creation

### Model Constraints
From the Post model:
```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
```

---

## Complete Testing Workflow

### 1. Create User Accounts
```bash
python manage.py createsuperuser
```
Create at least 2 users to test author-only permissions.

### 2. Test Post Creation
1. Log in as User A
2. Create a new post
3. Verify it appears in the post list

### 3. Test Post Viewing
1. Log out
2. View the post list (should work without login)
3. Click on a post to view details (should work without login)

### 4. Test Post Editing
1. Log in as User A (post author)
2. Edit the post
3. Verify changes are saved
4. Log in as User B (not the author)
5. Try to access the edit URL directly
6. Verify you get 403 Forbidden

### 5. Test Post Deletion
1. Log in as User A (post author)
2. Delete the post
3. Verify it's removed from the list
4. Create another post
5. Log in as User B (not the author)
6. Try to access the delete URL directly
7. Verify you get 403 Forbidden

---

## File Structure
```
django_blog/
├── blog/
│   ├── views.py              # Class-based views for CRUD
│   ├── urls.py               # URL patterns
│   ├── models.py             # Post model
│   └── templates/
│       └── blog/
│           ├── post_list.html
│           ├── post_detail.html
│           ├── post_form.html
│           └── post_confirm_delete.html
└── BLOG_POST_MANAGEMENT.md   # This documentation
```

---

## Troubleshooting

**Problem**: Can't create posts
**Solution**: Make sure you're logged in. The create view requires authentication.

**Problem**: Can't edit someone else's post
**Solution**: This is intentional. Only the post author can edit their posts (UserPassesTestMixin).

**Problem**: Getting 403 Forbidden when trying to edit/delete
**Solution**: You're not the author of that post. Only authors can edit/delete their own posts.

**Problem**: Posts not appearing in list
**Solution**: Make sure posts exist in the database. Create a post via the admin panel or create view.

---

## Future Enhancements

Potential improvements:
- Add categories/tags for posts
- Implement comments on posts
- Add search functionality
- Include pagination for post list
- Add rich text editor for content
- Allow image uploads
- Implement draft/publish status
- Add post scheduling