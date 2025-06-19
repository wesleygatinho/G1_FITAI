import uuid
from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr

# --- Schemas Base ---
# Propriedades compartilhadas por todos os schemas de usuário
class UserBase(BaseModel):
    email: EmailStr
    nome: Optional[str] = None
    data_nascimento: Optional[date] = None
    altura_cm: Optional[float] = None
    peso_kg: Optional[float] = None
    sexo: Optional[str] = None

# --- Schemas para Criação ---
# Schema usado ao criar um novo usuário (ex: recebendo da API)
class UserCreate(UserBase):
    password: str

# --- Schemas para Atualização ---
# Schema usado para atualizar um usuário
class UserUpdate(UserBase):
    pass

# --- Schemas para Leitura ---
# Propriedades que serão retornadas pela API (não inclui a senha!)
class UserInDBBase(UserBase):
    id: uuid.UUID
    is_active: bool
    is_superuser: bool
    is_verified: bool
    
    class Config:
        orm_mode = True # Permite que o Pydantic leia dados de modelos SQLAlchemy

# Schema principal para retornar um usuário na API
class User(UserInDBBase):
    pass