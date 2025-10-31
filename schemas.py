from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    doc_number: str
    password: str
    username: str
    full_name: str

class UserResponse(BaseModel):
    id: int
    email: str
    doc_number: str
    username: str
    full_name: str
    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    login: str
    password: str

class PasswordRecovery(BaseModel):
    document: str
    email: EmailStr
    new_password: str
