from token import OP
from typing import Optional
from sqlmodel import Session, select 

from app.models.order import Order, OrderItem 
from app.models.cart import CartItem
from app.models.product import Product 


def create_order_from_cart(session:Session, user_id: int) -> Optional[Order]:
    cart_items = list(session.exec(
        select(CartItem).where(CartItem.user_id == user_id)
    )).all()

    if not cart_items: 
        return None 
    
    total_price = 0.0 
    order_items_data = []

    for item in cart_items:
        product = session.get(Product, item.product_id)

        if product and product.is_active: 
            price = product.price 
            total_price += price * item.quantity 
            order_items_data.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price_at_moment": price
            })
    
    if not order_items_data:
        return None 
    
    order = Order(
        user_id = user_id,
        total_price = round(total_price, 2),
        status = "created"
    )

    session.add(order)
    session.commit()
    session.refresh(order)

    for data in order_items_data:
        order_item = OrderItem(order_id=order.id, **data)
        session.add(order_item)

    for item in cart_items:
        session.delete(item)

    session.refresh(order)
    return order


def get_all_orders(session: Session) -> list[Order]:
    statement = select(Order).order_by(Order.created_at.desc())
    return list(session.exec(statement).all())


def get_user_orders(session: Session, user_id: int) -> list[Order]:
    statement = select(Order).where(Order.user_id == user_id).order_by(Order.created_at.desc())
    return list(session.exec(statement).all())


def get_order_by_id(session: Session, order_id: int) -> Optional[Order]: 
    return session.get(Order, order_id)


def get_order_items(session: Session, order_id: int) -> list[OrderItem]:
    statement = select(OrderItem).where(OrderItem.order_id == order_id)
    return list(session.exec(statement).all())


def update_order_status(session: Session, order_id: int, status: str) -> Optional[Order]:
    order = session.get(Order, order_id)
    
    if not order:
        None 

    order.status = status 
    session.add(order)
    session.commit()
    session.refresh(order)

    return order





