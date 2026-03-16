from sqlmodel import Session, select 
from app.models.user import User 
from app.core.security import hash_password, verify_password, create_access_token


def register_user(session: Session, name: str, email: str, password: str) -> User:
    existing = session.exec(select(User).where(User.email == email)).first()

    if existing:
        raise ValueError("Пользователь с таким email уже существует")
    
    user = User(
        name=name,
        email=email,
        hashed_password=hash_password(password),
        role="user"
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user 


def authenticate_user(session: Session, email: str, password: str):
    user = session.exec(select(User).where(User.email == email)).first()

    if not user:
        return None 
    
    if not verify_password(password, user.hashed_password):
        return None 
    
    return user


def get_user_by_id(session: Session, user_id: int):
    return session.get(User, user_id)


def get_user_by_email(session: Session, email: str):
    return session.exec(select(User).where(User.email == email)).first()


def create_token_for_user(user: User) -> str:
    return create_access_token(data={"sub": str(user.id), "role": user.role})




