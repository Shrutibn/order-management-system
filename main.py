import time
import queue
import threading
from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import List
from dependencies.database_manager import db_manager
from dependencies import constants
from dependencies.authenticator import authenticator
from models.order import Order
from handlers import common_handler

# FastAPI app setup
app = FastAPI()

# Queue setup
order_queue = queue.Queue()


# Pydantic models
class OrderCreate(BaseModel):
    user_id: str
    item_ids: List[str]
    total_amount: float

class OrderStatus(BaseModel):
    order_id: str
    order_status: str

class Metrics(BaseModel):
    total_orders: int
    completed_orders: int
    pending_orders: int
    processing_orders: int
    average_processing_time: float

# API to create an order
@app.post("/order", response_model=OrderStatus)
async def create_order(order: OrderCreate, username: str = Depends(authenticator.validate), request: Request = None):
    try:
        db = db_manager.get_db(constants.db_url)
        new_order = Order(user_id=order.user_id, item_ids=str(order.item_ids), total_amount=order.total_amount, order_status='Pending')
        db.add(new_order)
        db.commit()
        new_order.order_id = common_handler.get_order_id(new_order.id)
        db.commit()
        db.refresh(new_order)

        # Add to the queue for asynchronous processing
        order_queue.put(new_order.order_id)

        db.close()

        return {"order_id": new_order.order_id, "order_status": new_order.order_status}
    except Exception as e:
        print(f"Exception occurred in create order api as {e}")
        raise HTTPException(status_code=500, detail="Internal Error")


# API to get order order_status
@app.get("/order/{order_id}", response_model=OrderStatus)
async def get_order_status(order_id: str, username: str = Depends(authenticator.validate), request: Request = None):
    try:
        db = db_manager.get_db(constants.db_url)
        order = db.query(Order).filter(Order.order_id == order_id).first()
        db.close()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        return {"order_id": order.order_id, "order_status": order.order_status}
    except Exception as e:
        print(f"Exception occurred in get order status api : {e}")
        raise HTTPException(status_code=500, detail="Internal Error")


# API to get metrics
@app.get("/metrics", response_model=Metrics)
async def get_metrics(username: str = Depends(authenticator.validate), request: Request = None):
    try:
        db = db_manager.get_db(constants.db_url)
        total_orders = db.query(Order).count()
        completed_orders = db.query(Order).filter(Order.order_status == 'Completed').count()
        pending_orders = db.query(Order).filter(Order.order_status == 'Pending').count()
        processing_orders = db.query(Order).filter(Order.order_status == 'Processing').count()

        # Calculate average processing time for completed orders
        completed_order_times = db.query(Order).filter(Order.order_status == 'Completed').all()
        if completed_order_times:
            total_processing_time = sum([(order.updated_at - order.created_at).total_seconds() for order in completed_order_times])
            average_processing_time = total_processing_time / len(completed_order_times)
        else:
            average_processing_time = 0

        db.close()

        return {
            "total_orders": total_orders,
            "completed_orders": completed_orders,
            "pending_orders": pending_orders,
            "processing_orders": processing_orders,
            "average_processing_time": average_processing_time
        }
    except Exception as e:
        print(f"Exception occurred in get metrics api as {e}")
        raise HTTPException(status_code=500, detail="Internal Error")

# Function to process orders asynchronously
def process_orders():
    while True:
        order_id = order_queue.get()
        if order_id is None:
            break

        db = db_manager.get_db(constants.db_url)
        order = db.query(Order).filter(Order.order_id == order_id).first()

        if order and order.order_status == 'Pending':
            # Simulate order processing
            order.order_status = 'Processing'
            db.commit()
            time.sleep(constants.processing_delay)  # Simulate processing delay

            order.order_status = 'Completed'
            db.commit()

        db.close()
        order_queue.task_done()

# Start the queue processing in a separate thread
order_processing_thread = threading.Thread(target=process_orders, daemon=True)
order_processing_thread.start()

# to test main.py file by python main.py
# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
