from typing import Optional
from sqlmodel import SQLModel, Field 

class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)
    description: str = Field(default="", max_length=500)