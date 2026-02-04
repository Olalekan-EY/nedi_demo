from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fast_api.config import DATABASE_URL

# SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # set to False in production
    future=True
)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
