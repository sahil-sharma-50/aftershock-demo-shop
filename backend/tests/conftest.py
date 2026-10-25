import shutil
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(monkeypatch):
    # tempfile instead of tmp_path: pytest's shared temp root can be unreadable on some Windows setups
    d = Path(tempfile.mkdtemp(prefix="demo-shop-test-"))
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{(d / 'test.db').as_posix()}")
    from app import db, repository

    repository.clear_caches()
    db.configure()
    from app.main import app

    with TestClient(app) as c:
        yield c
    db.engine.dispose()
    shutil.rmtree(d, ignore_errors=True)
