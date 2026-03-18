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


# Order #1  (user_id=42, total=15700, status="created")
# ├── OrderItem: product_id=5,  qty=2,  price=5500.00  → итого 11000
# ├── OrderItem: product_id=12, qty=1,  price=4700.00  → итого  4700
# └── ИТОГО: 15700

# Order #2  (user_id=42, total=4200, status="shipped")
# └── OrderItem: product_id=8,  qty=3,  price=1400.00  → итого  4200