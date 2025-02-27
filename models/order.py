from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

# Order Model
class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=False)
    item_ids = Column(String, nullable=False)
    total_amount = Column(Float, nullable=False)
    order_status = Column(String, nullable=False, default='Pending')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Order {self.order_id} {self.order_status}>"