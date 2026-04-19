from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models.model import Lead

router = APIRouter()


@router.get("/")
def get_leads(db: Session = Depends(get_db)):
    return db.query(Lead).all()