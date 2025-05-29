from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegistrationCreate(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: EmailStr
    created_by: str

class UserRegistrationResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    login_id: str
    password: str

class LoginResponse(BaseModel):
    message: str