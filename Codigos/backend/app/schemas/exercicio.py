import uuid
from typing import Optional
from pydantic import BaseModel

class ExercicioBase(BaseModel):
    """Schema base com os campos comuns de um exercício."""
    nome: str
    descricao: Optional[str] = None
    instrucoes: Optional[str] = None

class ExercicioCreate(ExercicioBase):
    """Schema usado para criar um novo exercício na base de dados."""
    pass

class ExercicioUpdate(ExercicioBase):
    """Schema usado para atualizar um exercício existente."""
    pass

class Exercicio(ExercicioBase):
    """
    Schema usado para ler um exercício da base de dados.
    Inclui o ID.
    """
    id: uuid.UUID

    class Config:
        from_attributes = True