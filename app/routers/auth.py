from urllib import response
from fastapi import APIRouter, Depends, Form, Request, Response

from fastapi.responses import RedirectResponse 
from sqlmodel import Session 

from app.core.database import get_session
from app.services.auth_service import create_token_for_user, register_user, authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def post_login(
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)):

    user = authenticate_user(session, email, password)
    if not user:
        return RedirectResponse(url="/login?error=Неверный email или пароль", status_code=303)
    

    token = create_access_token(user)

    response = RedirectResponse(url="/profile", status_code=303)
    response.set_cookie(key="access_token", value=token, httponly=True, max_age=86400)
    return response 


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response 


@router.post("/register")
def post_register(
    request: Request, 
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    password_confirm: str = Form(...),
    session: Session = Depends(get_session)
):
    errors = []

    if not name.strip():
        errors.append("Имя не может быть пустым")
    if len(password) < 6:
        errors.append("Длина пароля не может быть меньше 6 символов")
    if password != password_confirm:
        errors.append("Пароли не совпадают")

    if errors: 
        return RedirectResponse(url=f"/register?error={"|".join(errors)}", status_code=303)
    
    try:
        user = register_user(session, name.strip(), email, password)
        token = create_token_for_user(user)
        response = RedirectResponse(url="/profile", status_code=303)
        response.set_cookie(key="access_token", value=token, httponly=True, max_age=86400)

        return response 
    
    except Exception as e:
        return RedirectResponse(url=f"/register?error={str(e)}", status_code=303)
    
