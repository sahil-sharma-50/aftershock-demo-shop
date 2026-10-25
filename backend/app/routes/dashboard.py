from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import repository as repo
from ..db import get_session

router = APIRouter()


@router.get("/dashboard")
def dashboard(s: Session = Depends(get_session)):
    return repo.dashboard_stats(s)
