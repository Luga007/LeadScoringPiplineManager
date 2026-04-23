from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.model import Lead

router = APIRouter()


@router.get("/")
def get_analytics(db: Session = Depends(get_db)):
    leads = db.query(Lead).all()

    if not leads:
        return {
            "total_leads": 0,
            "avg_conversion": 0,
            "high_priority_count": 0,
            "total_value": 0
        }

    high_priority = [l for l in leads if l.conversion_probability > 0.7]

    return {
        "total_leads": len(leads),
        "avg_conversion": round(
            sum(l.conversion_probability for l in leads) / len(leads), 2
        ),
        "high_priority_count": len(high_priority),
        "total_value": sum(l.budget or 0 for l in leads)
    }