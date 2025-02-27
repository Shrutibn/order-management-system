# **Order Management System - FastAPI**

### **Overview**
1. This is a backend system for managing and processing orders in an e-commerce platform using FastAPI. It supports:
2. Order creation and retrieval via RESTful APIs.
3. Asynchronous order processing using an in-memory queue.
4. Order status tracking.
5. Key metrics reporting (total orders, processing time, etc.).

### **Setup & Installation**

#### 1.Clone the Repository
  git clone <GITHUB_REPO_LINK>
  cd order-management-system

#### 2.Create & Activate Virtual Environment
python -m venv venv
source venv/bin/activate  # For Mac/Linux
venv\Scripts\activate  # For Windows

#### 3.Install Dependencies
pip install -r requirements.txt

#### 4.Set Up Database (SQLite/PostgreSQL/MySQL)
Modify .env file with the database connection URL:
DATABASE_URL=mysql+pymysql://user:password@localhost/dbname  # For MySQL
DATABASE_URL=sqlite:///./orders.db  # For SQLite
DATABASE_URL=postgresql://user:password@localhost/dbname  # For PostgreSQL

#### 5.Run the Application
uvicorn main:app --reload
Server will start at: http://127.0.0.1:8000

#### 6.API Endpoints

##### a.Create an Order
Endpoint: POST /order

Request:
{
  "user_id": "user123",
  "item_ids": [101, 102],
  "total_amount": 250.75
}

cURL:
curl --location 'http://127.0.0.1:8000/order' \
--header 'Content-Type: application/json' \
--header 'Authorization: ••••••' \
--data '{
    "user_id" : "user123",
    "item_ids": [101, 102],
    "total_amount": 250.75
}'

Response:
{
  "order_id": "ORD4254",
  "order_status": "Pending"
}

##### b.Get Order Status
Endpoint: GET /order/{order_id}

Example Curl:
curl --location 'http://127.0.0.1:8000/order/ORD4254' \
--header 'Authorization: ••••••'

Response:
{
  "order_id": "ORD4254",
  "order_status": "Processing"
}

##### c. Get Order Metrics

Endpoint: GET /metrics

Example Curl:
curl --location 'http://127.0.0.1:8000/metrics' \
--header 'Authorization: ••••••'

Response:
{
  "total_orders": 100,
  "average_processing_time": 2.5,
  "pending_orders": 10,
  "processing_orders": 5,
  "completed_orders": 85
}

### Design Decisions & Trade-offs

##### 1.Database Choice
Used MySQL but supports SQLite/PostgresSQL

##### 2.Asynchronous Processing
Used Python queue.Queue for in-memory processing.
Trade-off: Does not persist orders if the app crashes; a message broker like Redis would be more robust.

##### 3.API Framework - FastAPI
Chosen for high performance (async support) and automatic documentation generation.
Alternative: Flask (slower but simpler for smaller applications).

### Assumptions
1. Each order has a unique order_id.
2. Orders transition through statuses: Pending → Processing → Completed.
3. Only basic authentication is implemented for now (extendable with JWT).
4. Kept 2 seconds delay to change order state from Processing to Completed .
5. kept hard coded client_id and client_secret in constants.py file (should be kept in enterprise client table) .
6. Version of requirements provided in requirements.txt by considering python3.10 .

### GitHub Repository
The full project code is available at:
GitHub Repo Link

### Running Tests
Run unit tests using:
pytest unit_test.py