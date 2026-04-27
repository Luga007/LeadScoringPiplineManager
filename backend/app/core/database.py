import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -----------------------
# DATABASE URL
# -----------------------
DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. "
        "Add it in your environment variables (Render / .env)."
    )


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # checks connection before using it
    pool_size=10,
    max_overflow=20,
    future=True
)

# -----------------------
# SESSION
# -----------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -----------------------
# BASE MODEL
# -----------------------
Base = declarative_base()

# -----------------------
# FASTAPI DEPENDENCY
# -----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()