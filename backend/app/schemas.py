from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict

class AnnotatedTextCreate(BaseModel):
    original_text: str
    annotated_text: str
    entities: List[Dict[str, str]]

class AnnotatedTextResponse(AnnotatedTextCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True