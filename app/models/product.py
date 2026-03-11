from datetime import datetime 
from typing import Optional
from sqlmodel import SQLModel, Field 


class Product(SQLModel, table=True):
    __tablename__ = "products"


    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    short_description: str = Field(default="", max_length=300)
    full_description: str = Field(default="")
    price: float = Field(ge=0)
    image_url: str = Field(default="/static/images/no-image.png")
    stock: int = Field(default=0, ge=0)
    category_id: int = Field(foreign_key="categories.id")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now())