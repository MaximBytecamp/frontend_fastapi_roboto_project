from typing import Optional 
from app.models import user
from sqlmodel import Session, select

from app.models.cart import CartItem 
from app.models.product import Product

def add_to_cart(session: Session, user_id: int, product_id: int, quantity: int = 1) -> CartItem:
    existing = session.exec(
        select(CartItem).where(
            CartItem.user_id == user_id,
            CartItem.product_id == product_id
        )
    ).first()

    if existing: 
        existing.quantity += quantity 
        session.add(existing)
        session.commit()
        session.refresh(existing)
        return existing
    
    else:
        cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        session.add(cart_item)
        session.commit()
        session.refresh(cart_item)
        return cart_item
    

def get_cart_items(session: Session, user_id: int) -> list[dict]:
    cart_items = list(session.exec(
        select(CartItem).where(CartItem.user_id == user_id)
    ).all())

    result = []
    for item in cart_items:
        product = session.get(Product, item.product_id)
        if product:
            result.append({
                "id": item.id,
                "product_id": item.product_id,
                "product_name": product.product_name,
                "product_image": product.image_url,
                "price": product.price, 
                "quantity": item.quantity,
                "subtotal": round(product.price * item.quantity, 2)
            }
            )
    return result 

def get_cart_total(session: Session, user_id: int) -> float:
    items = get_cart_items(session, user_id)
    return round(sum(item["subtotal"] for item in items), 2)


def get_cart_count(session: Session, user_id: int) -> int: 
    cart_items = list(session.exec(
        select(CartItem).where(CartItem.user_id == user_id)
    ).all())

    return sum(item.quantity for item in cart_items)

