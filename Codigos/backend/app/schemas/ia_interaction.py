"""
@file ia_interaction.py
@brief Define os schemas Pydantic para a entidade RegistroInteracaoIA.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class RegistroInteracaoIABase(BaseModel):
    """Schema base que define os campos comuns de uma interação com a IA.

    Attributes:
        prompt_usuario (str): O prompt ou pergunta enviado pelo utilizador para a IA.
        resposta_ia (str): A resposta de texto gerada pela IA.
    """
    prompt_usuario: str
    resposta_ia: str

class RegistroInteracaoIACreate(RegistroInteracaoIABase):
    """Schema usado para validar os dados ao criar um novo registo de interação."""
    # Herda todos os campos de RegistroInteracaoIABase.
    pass

class RegistroInteracaoIA(RegistroInteracaoIABase):
    """Schema usado para representar um registo de interação lido da base de dados.

    Attributes:
        id (uuid.UUID): ID único do registo de interação.
        data (datetime): Data e hora em que a interação ocorreu, gerada automaticamente.
        user_id (uuid.UUID): ID do utilizador que realizou a interação.
    """
    id: uuid.UUID
    data: datetime
    user_id: uuid.UUID

    class Config:
        """Configuração Pydantic para permitir a criação a partir de atributos do modelo ORM."""
        from_attributes = True
