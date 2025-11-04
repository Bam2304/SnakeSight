from typing import Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings

engine = create_engine(
	settings.DATABASE_URL,
	connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
	pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
	pass

def get_db() -> Any:
	"""TODO: Add description."""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
