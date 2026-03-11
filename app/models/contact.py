from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class ContactMessage(SQLModel, table=True):
    __tablename__ = "contact_messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    email: str = Field(max_length=255)
    subject: str = Field(max_length=300)
    message: str
    created_at: datetime = Field(default_factory=lambda:datetime.now())


    
