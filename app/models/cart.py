from typing import Optional
from sqlmodel import SQLModel, Field 

class CartItem(SQLModel, table=True):
    __tablename__ = "cart_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    product_id: int = Field(foreign_key="products.id")
    quantity: int = Field(default=1, ge=1)


# users           cart_items
# ──────          ──────────────────────────
# id=1  ──────┬── id=1, user_id=1, product_id=5, quantity=2
#             ├── id=2, user_id=1, product_id=12, quantity=1
#             └── id=3, user_id=1, product_id=8, quantity=3