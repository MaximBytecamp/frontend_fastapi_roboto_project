from datetime import datetime 
from typing import Optional
from sqlmodel import SQLModel, Field 

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    email: str = Field(max_length=255, unique=True, index=True)
    hashed_password: str 
    role: str = Field(default="user")
    created_at: datetime = Field(default_factory=lambda: datetime.now())