from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from . import database, models, crud, schemas

# Initialize FastAPI
app = FastAPI(title="NER Backend with GLiNER", version="0.1.0")

# Create tables
models.Base.metadata.create_all(bind=database.engine)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Load GLiNER model (do this once at startup)
@app.on_event("startup")
def load_gliner():
    global gliner
    from gliner import GLiNER
    app.state.gliner = GLiNER.from_pretrained("urchade/gliner_small-v1.1")

# Helper: Annotate text with entities
def annotate_text(text: str, model) -> tuple:
    predictions = model.predict_entities(text, labels=["person", "organization", "location", "date"], threshold=0.3)
    entities = []
    annotated_text = text
    offset = 0

    # Sort by start position to handle overlaps
    predictions.sort(key=lambda x: x['start'])

    for ent in predictions:
        start = ent['start'] + offset
        end = ent['end'] + offset
        label = ent['label']
        conf = ent['score']

        # Wrap entity in annotation
        replacement = f"[{text[ent['start']:ent['end']]}]({label}:{conf:.2f})"
        annotated_text = annotated_text[:start] + replacement + annotated_text[end:]
        offset += len(replacement) - (ent['end'] - ent['start'])  # adjust offset

        entities.append({
            "text": ent['text'],
            "label": label,
            "confidence": f"{conf:.2f}",
            "start": ent['start'],
            "end": ent['end']
        })

    return annotated_text, entities

# API Endpoint
@app.post("/ner", response_model=schemas.AnnotatedTextResponse)
def run_ner(data: dict, db: Session = Depends(get_db)):
    text = data.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    model = app.state.gliner
    annotated_text, entities = annotate_text(text, model)

    db_record = crud.AnnotatedTextCreate(
        original_text=text,
        annotated_text=annotated_text,
        entities=entities
    )
    saved = crud.create_annotated_text(db=db, data=db_record)

    return saved

@app.get("/ner", response_model=list[schemas.AnnotatedTextResponse])
def list_annotated_texts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_annotated_texts(db, skip=skip, limit=limit)