import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(autoflush=False, expire_on_commit=False)
engine = None


def configure(url: str | None = None):
    """(Re)bind the engine from DATABASE_URL; SessionLocal stays the same object."""
    global engine
    url = url or os.environ.get("DATABASE_URL", "sqlite:///./dev.db")
    if url.startswith("sqlite"):
        kwargs = {"connect_args": {"check_same_thread": False}}
    else:
        kwargs = {"pool_pre_ping": True}
    engine = create_engine(url, **kwargs)
    SessionLocal.configure(bind=engine)
    return engine


def get_session():
    with SessionLocal() as s:
        yield s


configure()
