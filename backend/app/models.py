from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AnnotatedText(Base):
    __tablename__ = "annotated_texts"

    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text, nullable=False)
    annotated_text = Column(Text, nullable=False)
    entities = Column(Text, nullable=False)  # JSON string
    user_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)