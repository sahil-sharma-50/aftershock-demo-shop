from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from .. import repository as repo
from ..db import get_session

router = APIRouter()


class ProductIn(BaseModel):
    name: str
    price: float
    stock: int = 0


class ProductUpdate(BaseModel):
    name: str
    price: float


class StockDelta(BaseModel):
    delta: int


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    price: float
    stock: int


def _call(fn, *args):
    try:
        return fn(*args)
    except repo.NotFound as e:
        raise HTTPException(404, str(e))
    except repo.InsufficientStock as e:
        raise HTTPException(409, str(e))


@router.get("/products", response_model=list[ProductOut])
def list_products(q: str | None = None, s: Session = Depends(get_session)):
    return repo.list_products(s, q)


@router.post("/products", response_model=ProductOut, status_code=201)
def create_product(body: ProductIn, s: Session = Depends(get_session)):
    return repo.create_product(s, body.name, body.price, body.stock)


@router.get("/products/{id}", response_model=ProductOut)
def get_product(id: int, s: Session = Depends(get_session)):
    return _call(repo.get_product, s, id)


@router.put("/products/{id}", response_model=ProductOut)
def update_product(id: int, body: ProductUpdate, s: Session = Depends(get_session)):
    return _call(repo.update_product, s, id, body.name, body.price)


@router.post("/products/{id}/stock", response_model=ProductOut)
def adjust_stock(id: int, body: StockDelta, s: Session = Depends(get_session)):
    return _call(repo.adjust_stock, s, id, body.delta)
