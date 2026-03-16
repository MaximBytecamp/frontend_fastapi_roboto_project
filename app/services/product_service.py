from typing import Optional
from sqlmodel import Session, select 
from app.models.product import Product 
from app.models.category import Category 

def get_all_products(session: Session, category_id: Optional[int] = None, search: Optional[str]=None, only_active: bool = True) -> list[Product]:
    statement = select(Product)
    if only_active: 
        statement = statement.where(Product.is_active == True)

    if category_id: 
        statement = statement.where(Product.category_id == category_id)

    if search:
        statement = statement.where(Product.name.ilike(f"%{search}%"))


    statement = statement.order_by(Product.created_at.desc())
    return list(session.exec(statement).all())

    

def create_product(session: Session, **kwargs) -> Product:
    product = Product(**kwargs)
    session.add(product)
    session.commit()
    session.refresh(product)

    return product 


def delete_product(session: Session, product_id: int) -> bool: 
    product = session.get(Product, product_id)

    if not product: 
        return None 
    
    session.delete(product)
    session.commit()
    return True 

def update_product(session: Session, product_id: int, **kwargs) -> Optional[Product]:
    product = session.get(Product, product_id)

    if not product:
        return None 
    
    for key, value in kwargs.items(): #[("key", "value")]
        setattr(product, key, value)



def get_all_categories(session: Session) -> list[Category]:
    return list(session.exec(select(Category)).all())


def get_category_by_id(session: Session, category_id: int) -> Optional[Category]:
    return session.get(Category, category_id)


def get_popular_products(session: Session , limit: int =  6) -> list[Product]:
    statement = select(Product).where(Product.is_active == True).limit(limit)
    return list(session.exec(statement).all())


