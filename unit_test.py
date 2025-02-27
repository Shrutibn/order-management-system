import pytest
from fastapi.testclient import TestClient
from dependencies import constants
from main import app
from dependencies.database_manager import db_manager
from models.order import Order
import queue
import base64
from handlers import common_handler

# Create a **test database**
TEST_DATABASE_URL = "" # provide test database url

# Use an in-memory queue for testing
test_order_queue = queue.Queue()

client = TestClient(app)  # Test client for API requests


# ----------------- TESTS -----------------

# ✅ **Test Order Creation API**
def test_create_order():
    order_data = {
        "user_id": "user123",
        "item_ids": [101, 102],
        "total_amount": 250.75
    }
    auth = f"{constants.valid_username}:{constants.valid_password}"
    encoded_auth = base64.b64encode(auth.encode()).decode()
    headers = {"Authorization": f"Basic {encoded_auth}"}

    response = client.post("/order", json=order_data, headers=headers)
    assert response.status_code == 200  # Check if order was created successfully

    data = response.json()
    assert "order_id" in data
    assert data["order_status"] == "Pending"


# ✅ **Test Fetching Order Status**
def test_get_order_status():
    # First, create an order
    order_data = {
        "user_id": "user123",
        "item_ids": [101, 102],
        "total_amount": 250.75
    }
    auth = f"{constants.valid_username}:{constants.valid_password}"
    encoded_auth = base64.b64encode(auth.encode()).decode()
    headers = {"Authorization": f"Basic {encoded_auth}"}
    create_response = client.post("/order", json=order_data, headers=headers)
    order_id = create_response.json()["order_id"]

    # Fetch the order status
    response = client.get(f"/order/{order_id}", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["order_id"] == order_id
    assert data["order_status"] in ["Pending", "Processing", "Completed"]


# ✅ **Test Metrics API**
def test_get_metrics():
    auth = f"{constants.valid_username}:{constants.valid_password}"
    encoded_auth = base64.b64encode(auth.encode()).decode()
    headers = {"Authorization": f"Basic {encoded_auth}"}
    response = client.get("/metrics", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "total_orders" in data
    assert "average_processing_time" in data
    assert "pending_orders" in data
    assert "processing_orders" in data
    assert "completed_orders" in data


# ✅ **Test Database Operations (Directly)**
def test_database_operations():
    db = db_manager.get_db(TEST_DATABASE_URL)

    # Insert test order
    new_order = Order(user_id="ok_user", item_ids="[201, 202]", total_amount=99.99, order_status="Pending")
    db.add(new_order)
    db.commit()
    new_order.order_id = common_handler.get_order_id(new_order.id)
    db.commit()
    db.refresh(new_order)

    # Fetch order from database
    retrieved_order = db.query(Order).filter_by(user_id="ok_user").first()
    assert retrieved_order is not None
    assert retrieved_order.order_status == "Pending"


# ✅ **Test Queue Processing**
def test_queue_processing():
    test_order_queue.put("test_order_123")  # Simulate adding an order to queue
    assert not test_order_queue.empty()  # Ensure queue has orders

    order_id = test_order_queue.get()  # Simulate order processing
    assert order_id == "test_order_123"  # Verify correct order ID was processed

