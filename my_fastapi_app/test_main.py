from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    """Test health check / root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI application!"}

def test_read_item():
    """Test reading item by ID and query param."""
    response = client.get("/items/10?q=laptop")
    assert response.status_code == 200
    assert response.json() == {"item_id": 10, "query_param": "laptop"}

def test_create_item():
    """Test creating an item via POST."""
    payload = {
        "name": "Mechanical Keyboard",
        "description": "RGB mechanical keyboard",
        "price": 100.0,
        "tax": 10.0
    }
    response = client.post("/items/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Item 'Mechanical Keyboard' created successfully!"
    assert data["total_price"] == 110.0
    assert data["name"] == "Mechanical Keyboard"
