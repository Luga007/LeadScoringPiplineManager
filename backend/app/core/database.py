from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Example:
# postgresql://username:password@localhost:5432/dbname

DATABASE_URL = "postgresql+psycopg2://postgres:your_password@localhost:5432/lead_db"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   #
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()