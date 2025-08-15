from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class AnnotatedText(Base):
    __tablename__ = "annotated_texts"

    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text, nullable=False)
    annotated_text = Column(Text, nullable=False)
    entities = Column(Text, nullable=False)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)