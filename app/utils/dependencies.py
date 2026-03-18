from typing import Optional
from app.models import user
from fastapi import Request 
from sqlmodel import Session 

from app.core.security import decode_access_token 
from app.models.user import User 

def get_current_user(request: Request, session: Session) -> Optional[User]:
    token = request.cookies.get("access_token")
    
    if not token:
        return None 
    
    payload = decode_access_token(token)
    if not payload:
        return None 
    
    user_id = payload.get("sub")

    if not user_id:
        return None 
    
    try:
        user = session.get(User, int(user_id))
        return user 
    except Exception:
        return None 

