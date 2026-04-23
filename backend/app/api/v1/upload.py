from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import pandas as pd
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.model import Lead
from backend.app.services.ml_service import calculate_conversion_probability

router = APIRouter()


@router.post("/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        df = pd.read_csv(file.file)

        # 1. Clean duplicates inside CSV
        df = df.drop_duplicates(subset=["email"])

        # 2. Clear old data FIRST (important)
        db.query(Lead).delete()
        db.commit()

        leads_created = []

        for _, row in df.iterrows():
            lead = Lead(
                name=row.get("name"),
                email=row.get("email"),
                company=row.get("company"),
                industry=row.get("industry"),
                budget=row.get("budget", 0),
            )

            lead.conversion_probability = calculate_conversion_probability(lead)

            db.add(lead)
            leads_created.append(lead)

        db.commit()

        return {
            "message": f"{len(leads_created)} leads uploaded",
            "sample": [
                {
                    "name": l.name,
                    "probability": l.conversion_probability
                }
                for l in leads_created[:5]
            ]
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))