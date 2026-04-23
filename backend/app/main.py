from fastapi import FastAPI
from backend.app.core.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from backend.app.models.model import Lead, Interaction, ScoringHistory
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.v1 import leads, upload, analytics

app = FastAPI(
    title="Lead Scoring & Pipeline Manager",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables in Postgres
Base.metadata.create_all(bind=engine)

app.include_router(leads.router, prefix="/api/v1/leads", tags=["Leads"])
app.include_router(upload.router, prefix="/api/v1/upload", tags=["Upload"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])


@app.get("/")
def root():
    return {"message": "Lead Scoring API is running on PostgreSQL"}