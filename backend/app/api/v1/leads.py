from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models.model import Lead
from services.ml_service import calculate_conversion_probability

router = APIRouter()


from sqlalchemy import distinct

@router.get("/industries")
def get_industries(db: Session = Depends(get_db)):
    industries = db.query(distinct(Lead.industry)).all()

    return [i[0] for i in industries if i[0] is not None]

@router.get("/")
def get_leads(
    min_prob: float = 0,
    industry: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Lead)

    if min_prob:
        query = query.filter(Lead.conversion_probability >= min_prob)

    if industry:
        query = query.filter(Lead.industry == industry)

    return query.all()


@router.get("/{lead_id}")
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    return db.query(Lead).filter(Lead.id == lead_id).first()


@router.post("/{lead_id}/rescore")
def rescore_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not lead:
        return {"error": "Lead not found"}

    old_score = lead.conversion_probability
    new_score = calculate_conversion_probability(lead)

    lead.conversion_probability = new_score
    db.commit()

    return {"old_score": old_score, "new_score": new_score}