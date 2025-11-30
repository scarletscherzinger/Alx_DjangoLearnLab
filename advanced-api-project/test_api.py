import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

print("="*50)
print("Testing API Endpoints")
print("="*50)

# Test 1: Get all books (should work without authentication)
print("\n1. Testing GET /api/books/ (List all books)")
response = requests.get(f"{BASE_URL}/books/")
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 2: Get a single book (should work without authentication)
print("\n2. Testing GET /api/books/1/ (Get book detail)")
response = requests.get(f"{BASE_URL}/books/1/")
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 3: Try to create a book without authentication (should fail - 403)
print("\n3. Testing POST /api/books/create/ (Without authentication - should fail)")
new_book = {
    "title": "New Book",
    "publication_year": 2024,
    "author": 1
}
response = requests.post(f"{BASE_URL}/books/create/", json=new_book)
print(f"Status Code: {response.status_code} (Expected: 403 Forbidden)")
print(f"Response: {response.json()}")

print("\n" + "="*50)
print("Tests completed!")
print("="*50)