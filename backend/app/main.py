from fastapi import FastAPI
from core.database import engine, Base

from models.model import Lead, Interaction, ScoringHistory

from api.v1 import leads, upload, analytics

app = FastAPI(
    title="Lead Scoring & Pipeline Manager",
    version="1.0.0"
)

# Create tables in Postgres
Base.metadata.create_all(bind=engine)

app.include_router(leads.router, prefix="/api/v1/leads", tags=["Leads"])
app.include_router(upload.router, prefix="/api/v1/upload", tags=["Upload"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])


@app.get("/")
def root():
    return {"message": "Lead Scoring API is running on PostgreSQL"}