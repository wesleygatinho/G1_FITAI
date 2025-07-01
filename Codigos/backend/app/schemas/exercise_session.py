"""
@file exercise_session.py
@brief Define os schemas Pydantic para as entidades SessaoDeTreino e ItemSessao.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

import uuid
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Importa o schema Exercicio para ser usado de forma aninhada.
from .exercicio import Exercicio

class ItemSessaoBase(BaseModel):
    """Schema base para um item de uma sessão de treino.

    Attributes:
        series (int): Número de séries realizadas.
        repeticoes (int): Número de repetições por série.
        feedback_ia (Optional[str]): Feedback opcional gerado pela IA sobre a execução.
    """
    series: int
    repeticoes: int
    feedback_ia: Optional[str] = None

class ItemSessaoCreate(ItemSessaoBase):
    """Schema para validar os dados ao criar um novo item de sessão.

    Attributes:
        exercicio_id (uuid.UUID): ID do exercício ao qual este item de sessão está associado.
    """
    exercicio_id: uuid.UUID

class ItemSessao(ItemSessaoBase):
    """Schema para representar um item de sessão lido da base de dados.

    Attributes:
        id (uuid.UUID): ID único do item da sessão.
        exercicio (Exercicio): Objeto completo do exercício, aninhado para fornecer detalhes.
    """
    id: uuid.UUID
    exercicio: Exercicio

    class Config:
        """Configuração Pydantic para permitir a criação a partir de atributos do modelo ORM."""
        from_attributes = True

# --- Schemas para Sessão de Treino ---

class SessaoDeTreinoBase(BaseModel):
    """Schema base para uma sessão de treino, serve como base para outros schemas."""
    pass

class SessaoDeTreinoCreate(SessaoDeTreinoBase):
    """Schema para validar os dados ao criar uma nova sessão de treino.

    Attributes:
        itens (List[ItemSessaoCreate]): Lista de itens que compõem a sessão de treino a ser criada.
    """
    itens: List[ItemSessaoCreate]

class SessaoDeTreino(SessaoDeTreinoBase):
    """Schema para representar uma sessão de treino lida da base de dados.

    Attributes:
        id (uuid.UUID): ID único da sessão de treino.
        data_inicio (datetime): Data e hora de início da sessão, geradas automaticamente.
        data_fim (Optional[datetime]): Data e hora de fim da sessão, pode ser nula se a sessão estiver em andamento.
        itens (List[ItemSessao]): Lista dos itens da sessão, já formatados com os detalhes do exercício.
    """
    id: uuid.UUID
    data_inicio: datetime
    data_fim: Optional[datetime]
    itens: List[ItemSessao] = []

    class Config:
        """Configuração Pydantic para permitir a criação a partir de atributos do modelo ORM."""
        from_attributes = True
