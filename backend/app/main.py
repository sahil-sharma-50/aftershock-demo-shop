import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import db
from .models import Base
from .routes import dashboard, orders, products
from .seed import seed
from .telemetry import start_telemetry


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(db.engine)
    with db.SessionLocal() as s:
        seed(s)
    start_telemetry(enabled=os.getenv("TELEMETRY_DISABLED") != "1")
    yield


app = FastAPI(title="Demo Shop", lifespan=lifespan)
app.include_router(products.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"ok": True}
