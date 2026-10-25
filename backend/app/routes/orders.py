import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .. import repository as repo
from ..db import get_session

router = APIRouter()


class OrderIn(BaseModel):
    product_id: int
    quantity: int


class OrderOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    total: float
    created_at: datetime


@router.get("/orders", response_model=list[OrderOut])
def list_orders(s: Session = Depends(get_session)):
    return repo.list_orders(s)


@router.get("/orders/export.csv")
def export_orders(s: Session = Depends(get_session)):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["id", "product", "quantity", "total", "created_at"])
    for o in repo.list_orders(s):
        product = repo.get_product(s, o["product_id"])
        w.writerow([o["id"], product.name, o["quantity"], f"{o['total']:.2f}", o["created_at"].isoformat()])
    return Response(buf.getvalue(), media_type="text/csv")


@router.post("/orders", response_model=OrderOut, status_code=201)
def create_order(body: OrderIn, s: Session = Depends(get_session)):
    try:
        return repo.create_order(s, body.product_id, body.quantity)
    except repo.NotFound as e:
        raise HTTPException(404, str(e))
    except repo.InsufficientStock as e:
        raise HTTPException(409, str(e))
