import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

print("="*60)
print("Testing Filtering, Searching, and Ordering")
print("="*60)

# Test 1: Get all books (baseline)
print("\n1. GET all books (baseline)")
response = requests.get(f"{BASE_URL}/books/")
print(f"Status: {response.status_code}")
print(f"Books found: {len(response.json())}")

# Test 2: Filter by publication year
print("\n2. Filter by publication_year=1997")
response = requests.get(f"{BASE_URL}/books/?publication_year=1997")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 3: Search for books
print("\n3. Search for 'Potter'")
response = requests.get(f"{BASE_URL}/books/?search=Potter")
print(f"Status: {response.status_code}")
print(f"Books found: {len(response.json())}")
print(f"Titles: {[book['title'] for book in response.json()]}")

# Test 4: Order by title
print("\n4. Order by title (ascending)")
response = requests.get(f"{BASE_URL}/books/?ordering=title")
print(f"Status: {response.status_code}")
print(f"Titles in order: {[book['title'] for book in response.json()]}")

# Test 5: Order by publication year (descending)
print("\n5. Order by publication_year (descending)")
response = requests.get(f"{BASE_URL}/books/?ordering=-publication_year")
print(f"Status: {response.status_code}")
print(f"Years in order: {[(book['title'], book['publication_year']) for book in response.json()]}")

# Test 6: Combine filter, search, and ordering
print("\n6. Combine: search='Harry' + ordering=title")
response = requests.get(f"{BASE_URL}/books/?search=Harry&ordering=title")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

print("\n" + "="*60)
print("All tests completed!")
print("="*60)