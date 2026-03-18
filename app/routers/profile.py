from fastapi import APIRouter, Depends, Form, Request 
from fastapi.responses import RedirectResponse 
from sqlmodel import Session 

from app.core.database import get_session
from app.utils.dependencies import get_current_user


router = APIRouter(prefix="/profile", tags=["profile"])

@router.post("/update")
def profile_update(
    request: Request, 
    name: str = Form(...),
    session: Session = Depends(get_session)
):
    user = get_current_user(request, session)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    if not name.strip():
        return RedirectResponse(url="/profile?error=Имя не может быть пустым", status_code=303)
    

    user.name = name.strip()
    session.add(user)
    session.commit()

    return RedirectResponse(url="/profile?success=Профиль обновлен!", status_code=303)