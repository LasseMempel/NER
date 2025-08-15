from sqlalchemy.orm import Session
from . import models, schemas

def create_annotated_text(db: Session, data: schemas.AnnotatedTextCreate):
    db_text = models.AnnotatedText(
        original_text=data.original_text,
        annotated_text=data.annotated_text,
        entities=str(data.entities)  # Simple stringification; consider JSON field
    )
    db.add(db_text)
    db.commit()
    db.refresh(db_text)
    return db_text

def get_annotated_texts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AnnotatedText).offset(skip).limit(limit).all()