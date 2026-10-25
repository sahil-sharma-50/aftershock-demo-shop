from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import Order, Product


class NotFound(Exception):
    pass


class InsufficientStock(Exception):
    pass


# cache product reads; export iterates all orders and looks up each product
_product_cache: dict[int, Product] = {}
_list_cache: dict[str, list[Product]] = {}


def clear_caches() -> None:
    _product_cache.clear()
    _list_cache.clear()


def list_products(s: Session, q: str | None = None) -> list[Product]:
    key = (q or "").lower()
    if key in _list_cache:
        return list(_list_cache[key])
    stmt = select(Product).order_by(Product.id)
    if q:
        stmt = stmt.where(func.lower(Product.name).contains(q.lower(), autoescape=True))
    rows = list(s.scalars(stmt))
    for p in rows:
        s.expunge(p)
    _list_cache[key] = rows
    return list(rows)


def get_product(s: Session, id: int) -> Product:
    if id in _product_cache:
        return _product_cache[id]
    p = s.get(Product, id)
    if p is None:
        raise NotFound(f"Product {id} not found")
    s.expunge(p)
    _product_cache[id] = p
    return p


def _locked_product(s: Session, id: int) -> Product:
    p = s.scalars(select(Product).where(Product.id == id).with_for_update()).first()
    if p is None:
        raise NotFound(f"Product {id} not found")
    return p


def create_product(s: Session, name: str, price: float, stock: int) -> Product:
    p = Product(name=name, price=price, stock=stock)
    s.add(p)
    s.commit()
    return p


def update_product(s: Session, id: int, name: str, price: float) -> Product:
    p = s.get(Product, id)
    if p is None:
        raise NotFound(f"Product {id} not found")
    p.name, p.price = name, price
    s.commit()
    return p


def adjust_stock(s: Session, id: int, delta: int) -> Product:
    p = _locked_product(s, id)
    if p.stock + delta < 0:
        s.rollback()
        raise InsufficientStock("Not enough stock")
    p.stock += delta
    s.commit()
    clear_caches()
    return p


def _order_dict(o: Order, product_name: str) -> dict:
    return {
        "id": o.id,
        "product_id": o.product_id,
        "product_name": product_name,
        "quantity": o.quantity,
        "total": o.total,
        "created_at": o.created_at,
    }


def list_orders(s: Session) -> list[dict]:
    rows = s.execute(
        select(Order, Product.name).join(Product, Product.id == Order.product_id).order_by(Order.id.desc())
    ).all()
    return [_order_dict(o, name) for o, name in rows]


def create_order(s: Session, product_id: int, quantity: int) -> dict:
    p = _locked_product(s, product_id)
    if quantity < 1 or p.stock < quantity:
        s.rollback()
        raise InsufficientStock("Not enough stock")
    p.stock -= quantity
    o = Order(product_id=p.id, quantity=quantity, total=round(p.price * quantity, 2))
    s.add(o)
    s.commit()
    clear_caches()
    return _order_dict(o, p.name)


def dashboard_stats(s: Session) -> dict:
    return {
        "product_count": s.scalar(select(func.count(Product.id))) or 0,
        "stock_units": int(s.scalar(select(func.coalesce(func.sum(Product.stock), 0))) or 0),
        "order_count": s.scalar(select(func.count(Order.id))) or 0,
        "revenue": float(s.scalar(select(func.coalesce(func.sum(Order.total), 0))) or 0),
    }
