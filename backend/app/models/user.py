from typing import Optional
from beanie import Document
from pydantic import BaseModel, Field, EmailStr
import bcrypt

class User(Document):
    username: str = Field(..., unique=True)
    email: EmailStr = Field(..., unique=True)
    hashed_password: str
    nickname: str
    
    class Settings:
        name = "users"
    
    def verify_password(self, plain_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), self.hashed_password.encode('utf-8'))
    
    @staticmethod
    def hash_password(plain_password: str) -> str:
        return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# DTO
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    nickname: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    nickname: str
