from sqlalchemy.orm import Session
from . import models, schemas
import json

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_annotated_text(db: Session, original_text: str, annotated_text: str, entities: list, user_id: int):
    db_text = models.AnnotatedText(
        original_text=original_text,
        annotated_text=annotated_text,
        entities=json.dumps(entities),
        user_id=user_id
    )
    db.add(db_text)
    db.commit()
    db.refresh(db_text)
    return db_text

def get_annotated_texts(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.AnnotatedText).filter(models.AnnotatedText.user_id == user_id).offset(skip).limit(limit).all()