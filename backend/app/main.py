from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.database import engine, Base
from backend.app.models.model import Lead, Interaction, ScoringHistory
from backend.app.api.v1 import leads, upload, analytics


# -----------------------
# APP INIT
# -----------------------
app = FastAPI(
    title="Lead Scoring & Pipeline Manager",
    version="1.0.0"
)

# -----------------------
# CORS (for Streamlit + frontend)
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# SAFE DB INITIALIZATION
# (IMPORTANT FIX FOR RENDER CRASH)
# -----------------------
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# -----------------------
# ROUTES
# -----------------------
app.include_router(leads.router, prefix="/api/v1/leads", tags=["Leads"])
app.include_router(upload.router, prefix="/api/v1/upload", tags=["Upload"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])

# -----------------------
# HEALTH CHECK
# -----------------------
@app.get("/")
def root():
    return {
        "message": "Lead Scoring API is running on PostgreSQL 🚀"
    }