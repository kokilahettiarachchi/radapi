import requests
import json

# Define the base URL for the API
BASE_URL = "http://127.0.0.1:8000"

# Create a new item
def create_item(name: str, description: str):
    url = f"{BASE_URL}/items/"
    data = {
        "name": name,
        "description": description
    }
    response = requests.post(url, json=data)
    print("Create Response:", response.status_code, response.json())
    return response.json()

# Get all items
def get_items():
    url = f"{BASE_URL}/items/"
    response = requests.get(url)
    print("Get All Items Response:", response.status_code, response.json())
    return response.json()

# Get an item by ID
def get_item_by_id(item_id: int):
    url = f"{BASE_URL}/items/{item_id}/"
    response = requests.get(url)
    print(f"Get Item {item_id} Response:", response.status_code, response.json())
    return response.json()

# Update an item
def update_item(item_id: int, name: str, description: str):
    url = f"{BASE_URL}/items/{item_id}/"
    data = {
        "name": name,
        "description": description
    }
    response = requests.put(url, json=data)
    print(f"Update Item {item_id} Response:", response.status_code, response.json())
    return response.json()

# Delete an item
def delete_item(item_id: int):
    url = f"{BASE_URL}/items/{item_id}/"
    response = requests.delete(url)
    print(f"Delete Item {item_id} Response:", response.status_code, response.json())
    return response.status_code

# Run all tests
def run_tests():
    print("Running Tests...\n")
    
    # Test creating an item
    new_item = create_item("Test Item", "This is a test item")
    
    # Get all items (should include the new item)
    get_items()
    
    # Test getting an item by ID (using the ID of the newly created item)
    if 'id' in new_item:
        get_item_by_id(new_item['id'])
    
    # Test updating the item
    if 'id' in new_item:
        update_item(new_item['id'], "Updated Test Item", "Updated description")
    
    # Test deleting the item
    if 'id' in new_item:
        delete_item(new_item['id'])

    # Final list of items
    get_items()

if __name__ == "__main__":
    run_tests()