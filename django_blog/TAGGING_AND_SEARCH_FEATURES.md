# Tagging and Search Features Documentation

## Overview
This Django blog application includes tagging and search functionality to help users organize and discover content.

## Tagging System

### How to Add Tags to Posts

1. **When Creating a New Post:**
   - Navigate to "Create New Post"
   - Fill in the title and content
   - In the "Tags" field, enter tags separated by commas
   - Example: `django, python, web development`
   - Click "Save" to create the post with tags

2. **When Editing an Existing Post:**
   - Click "Edit Post" on any post you authored
   - Modify the tags in the "Tags" field
   - Tags can be added, removed, or modified
   - Click "Save" to update

### Viewing Posts by Tag

- Tags appear below post content on detail pages and in post listings
- Click any tag to view all posts with that tag
- The URL format is: `/tags/<tag_name>/`

## Search Functionality

### How to Search for Posts

1. **Using the Search Bar:**
   - Located at the top of the "Blog Posts" page
   - Enter keywords related to:
     - Post titles
     - Post content
     - Tag names
   - Click "Search" to see results

2. **Search Behavior:**
   - Search is case-insensitive
   - Searches across title, content, and tags simultaneously
   - Results show all posts matching any of the search criteria
   - If no posts match, a "No posts found" message appears

### Search URL
- Direct search URL format: `/search/?q=your_search_query`
- Example: `/search/?q=django`

## Features

### Tag Features
- **Multiple tags per post:** Posts can have unlimited tags
- **Automatic tag creation:** New tags are created automatically when entered
- **Tag reuse:** Existing tags can be applied to multiple posts
- **Clickable tags:** All tags are links to filtered views

### Search Features
- **Multi-field search:** Searches title, content, and tags
- **Partial matching:** Finds posts containing search terms anywhere in the text
- **Distinct results:** Each post appears only once in results, even if it matches multiple criteria

## Implementation Details

### Technologies Used
- **django-taggit:** Third-party package for tag management
- **Django Q objects:** For complex database queries in search
- **PostgreSQL:** Database backend (production)
- **SQLite:** Database backend (development)

### Models
- `Post` model includes `tags = TaggableManager()` field
- Tags are stored in separate tables managed by django-taggit

### Views
- `search_posts(request)`: Handles search queries
- `posts_by_tag(request, tag_name)`: Filters posts by tag

### URL Patterns
- `/search/`: Search results page
- `/tags/<str:tag_name>/`: Posts filtered by tag