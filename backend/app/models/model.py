from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    company = Column(String)
    industry = Column(String)

    budget = Column(Float)
    conversion_probability = Column(Float, default=0.0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    interactions = relationship("Interaction", back_populates="lead")


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))

    note = Column(String)
    score_change = Column(Float, default=0.0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    lead = relationship("Lead", back_populates="interactions")


class ScoringHistory(Base):
    __tablename__ = "scoring_history"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, index=True)

    old_score = Column(Float)
    new_score = Column(Float)

    reason = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())