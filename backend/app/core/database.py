from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base



from sqlalchemy.engine import URL

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="root",  # no need to encode
    host="localhost",
    port=5432,
    database="lead_db"
)

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