from sqlmodel import Session 
from app.models.contact import ContactMessage 

def save_contact_message(session: Session, name: str, email: str, subject: str, message: str) -> ContactMessage:
    msg = ContactMessage(
        name=name,
        email=email,
        subject=subject,
        message=message 
    )

    session.add(msg)
    session.commit()
    session.refresh(msg)
    return msg 


