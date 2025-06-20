import uuid
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from .exercicio import Exercicio

class ItemSessaoBase(BaseModel):
    series: int
    repeticoes: int
    feedback_ia: Optional[str] = None

class ItemSessaoCreate(ItemSessaoBase):
    # Para criar, ligamos ao exercício através do seu ID
    exercicio_id: uuid.UUID

class ItemSessao(ItemSessaoBase):
    id: uuid.UUID
    # Ao ler um item, incluímos os detalhes completos do exercício
    exercicio: Exercicio

    class Config:
        from_attributes = True

# --- Schemas para Sessão de Treino ---

class SessaoDeTreinoBase(BaseModel):
    pass

class SessaoDeTreinoCreate(SessaoDeTreinoBase):
    # Para criar uma sessão, recebemos uma lista de itens a serem criados
    itens: List[ItemSessaoCreate]

class SessaoDeTreino(SessaoDeTreinoBase):
    id: uuid.UUID
    data_inicio: datetime
    data_fim: Optional[datetime]
    # Ao ler uma sessão, ela vem com la lista de itens já formatada
    itens: List[ItemSessao] = []

    class Config:
        from_attributes = True