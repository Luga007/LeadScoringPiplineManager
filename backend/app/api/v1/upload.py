from fastapi import APIRouter, UploadFile, File, Depends
import pandas as pd
from sqlalchemy.orm import Session

from core.database import get_db
from models.model import Lead
from services.ml_service import calculate_conversion_probability

router = APIRouter()


@router.post("/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)

    created = 0

    for _, row in df.iterrows():
        lead = Lead(
            name=row.get("name"),
            email=row.get("email"),
            company=row.get("company"),
            industry=row.get("industry"),
            budget=row.get("budget", 0)
        )

        lead.conversion_probability = calculate_conversion_probability(lead)

        db.add(lead)
        created += 1

    db.commit()

    return {"message": f"{created} leads uploaded successfully"}