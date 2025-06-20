import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class RegistroInteracaoIABase(BaseModel):
    """Schema base com os campos comuns de uma interação com a IA."""
    prompt_usuario: str
    resposta_ia: str

class RegistroInteracaoIACreate(RegistroInteracaoIABase):
    """Schema usado para criar um novo registo de interação na base de dados."""
    pass

class RegistroInteracaoIA(RegistroInteracaoIABase):
    """
    Schema usado para ler um registo de interação da base de dados.
    Inclui o ID, a data e o ID do utilizador.
    """
    id: uuid.UUID
    data: datetime
    user_id: uuid.UUID

    class Config:
        from_attributes = True