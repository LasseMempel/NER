from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict

# User Schemas
class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int
    email: str

# NER Schema
class AnnotatedTextCreate(BaseModel):
    original_text: str
    annotated_text: str
    entities: List[Dict[str, str]]

class AnnotatedTextResponse(AnnotatedTextCreate):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True