from datetime import datetime
from token import OP
from typing import Optional
from sqlmodel import SQLModel, Field


class Order(SQLModel, table=True):
    __tablename__ = "orders"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    total_price: float = Field(default=0)
    status: str = Field(default="created")  # created, confirmed, shipped, completed, cancelled
    created_at: datetime = Field(default_factory=lambda: datetime.now())


class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    product_id: int = Field(foreign_key="products.id")
    quantity: int = Field(ge=1)
    price_at_moment: float = Field(ge=0)


