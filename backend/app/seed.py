from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import Order, Product

PRODUCTS = [
    ("Blue Mug", 12.00, 20),
    ("Red Mug", 12.00, 15),
    ("Notebook", 5.50, 40),
    ("Desk Plant", 18.00, 3),
    ("Pen Set", 9.00, 60),
    ("Wall Clock", 25.00, 7),
    ("Tote Bag", 14.00, 25),
    ("Water Bottle", 16.00, 2),
]
# (product name, quantity); the stock above is already the final value
ORDERS = [("Notebook", 2), ("Pen Set", 1), ("Tote Bag", 3)]


def seed(s: Session) -> None:
    if s.scalar(select(func.count(Product.id))):
        return
    s.add_all(Product(name=n, price=p, stock=st) for n, p, st in PRODUCTS)
    s.flush()
    by_name = {p.name: p for p in s.scalars(select(Product))}
    for name, qty in ORDERS:
        p = by_name[name]
        s.add(Order(product_id=p.id, quantity=qty, total=round(p.price * qty, 2)))
    s.commit()
