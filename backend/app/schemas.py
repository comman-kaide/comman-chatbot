from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime

# Chat schemas
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    context_used: Optional[List[Dict]] = None

# FAQ schemas
class FAQBase(BaseModel):
    question: str
    answer: str
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    is_active: bool = True

class FAQCreate(FAQBase):
    pass

class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None

class FAQResponse(FAQBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Document schemas
class DocumentBase(BaseModel):
    title: str
    content: str
    category: Optional[str] = None
    is_active: bool = True

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None

class DocumentResponse(DocumentBase):
    id: int
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str

# Chat History schemas
class ChatHistoryResponse(BaseModel):
    id: int
    session_id: str
    user_message: str
    bot_response: str
    context_used: Optional[Dict] = None
    created_at: datetime

    class Config:
        from_attributes = True
