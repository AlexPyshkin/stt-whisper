from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database URL - you'll need to update this with your actual database credentials
DATABASE_URL = "postgresql://developer:developer@postgres:5432/stt"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

class WhisperRecord(Base):
    __tablename__ = "whisper"
    __table_args__ = {"schema": "stt"}

    id = Column(Integer, primary_key=True, index=True)
    audio_data = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    transcribed_text = Column(String, nullable=True)
    correct_text = Column(String, nullable=True)
    is_processed = Column(Boolean, default=False)

# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 