from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import json
import os

from . import database, models, schemas, crud, auth
from .auth import get_current_user, create_access_token, authenticate_user

app = FastAPI(title="Secure NER Backend", version="1.0.0")

# CORS (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load GLiNER on startup
@app.on_event("startup")
async def load_gliner():
    global gliner
    from gliner import GLiNER
    model_path = "/app/gliner_model"
    if os.path.exists(model_path):
        app.state.gliner = GLiNER.from_pretrained(model_path)
    else:
        app.state.gliner = GLiNER.from_pretrained("knowledgator/gliner-x-large")
    print("🟢 GLiNER x-large model loaded!")

# Helper: Annotate text
async def annotate_text(text: str, model) -> tuple:
    predictions = model.predict_entities(text, labels=["person", "organization", "location", "date", "email", "phone"], threshold=0.3)
    entities = []
    annotated_text = text
    offset = 0

    predictions.sort(key=lambda x: x['start'])

    for ent in predictions:
        start = ent['start'] + offset
        end = ent['end'] + offset
        label = ent['label']
        conf = ent['score']
        replacement = f"[{ent['text']}]({label}:{conf:.2f})"
        annotated_text = annotated_text[:start] + replacement + annotated_text[end:]
        offset += len(replacement) - (ent['end'] - ent['start'])

        entities.append({
            "text": ent['text'],
            "label": label,
            "confidence": f"{conf:.2f}",
            "start": ent['start'],
            "end": ent['end']
        })

    return annotated_text, entities

# Routes
@app.post("/register", response_model=schemas.UserOut, status_code=201)
async def register(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.create_user(db, user)
    return db_user

@app.post("/login", response_model=schemas.Token)
async def login(credentials: schemas.UserLogin, db: Session = Depends(auth.get_db)):
    user = authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/ner", response_model=schemas.AnnotatedTextResponse)
async def run_ner(data: dict, db: Session = Depends(auth.get_db), user: models.User = Depends(get_current_user)):
    text = data.get("text")
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="No text provided")

    model = app.state.gliner
    annotated_text, entities = await annotate_text(text, model)

    saved = crud.create_annotated_text(
        db=db,
        original_text=text,
        annotated_text=annotated_text,
        entities=entities,
        user_id=user.id
    )

    return {
        "id": saved.id,
        "original_text": saved.original_text,
        "annotated_text": saved.annotated_text,
        "entities": json.loads(saved.entities),
        "user_id": saved.user_id,
        "created_at": saved.created_at
    }

@app.get("/ner", response_model=list[schemas.AnnotatedTextResponse])
async def get_my_texts(db: Session = Depends(auth.get_db), user: models.User = Depends(get_current_user)):
    return crud.get_annotated_texts(db, user.id)