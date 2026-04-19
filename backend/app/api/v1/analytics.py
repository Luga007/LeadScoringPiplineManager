from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models.model import Lead
from services.analytics_service import calculate_kpis

router = APIRouter()


@router.get("/")
def get_analytics(db: Session = Depends(get_db)):
    leads = db.query(Lead).all()

    return calculate_kpis(leads)