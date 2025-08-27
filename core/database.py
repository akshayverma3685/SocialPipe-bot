from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
from core.config import settings

engine = create_engine(settings.DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    platform = Column(String, index=True)
    category = Column(String, index=True)
    thread_key = Column(String, index=True)
    payload = Column(JSON)
    delivered = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

def init_db():
    Base.metadata.create_all(bind=engine)
