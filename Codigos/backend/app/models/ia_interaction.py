"""
@file ia_interaction.py
@brief Define o modelo SQLAlchemy para a tabela 'registro_interacao_ia'.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

import uuid
from sqlalchemy import Column, String, Text, ForeignKey, DateTime, UUID
from sqlalchemy.orm import relationship
from datetime import datetime

# Importa a Base declarativa a partir do módulo user para manter a ligação entre os modelos.
from .user import Base

class RegistroInteracaoIA(Base):
    """Modelo para a tabela 'registro_interacao_ia'.

    Armazena o histórico de todas as interações entre um utilizador e o serviço
    de IA generativa, guardando o prompt e a resposta correspondente.

    Attributes:
        id (UUID): ID único do registo de interação, gerado automaticamente.
        data (DateTime): Data e hora em que a interação ocorreu.
        prompt_usuario (Text): O prompt (pergunta) que o utilizador enviou para a IA.
        resposta_ia (Text): A resposta que a IA gerou para o prompt do utilizador.
        user_id (UUID): Chave estrangeira que liga o registo ao utilizador que fez a pergunta.
        owner (relationship): Relacionamento de volta para o utilizador.
    """
    # Nome da tabela na base de dados.
    __tablename__ = "registro_interacao_ia"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    prompt_usuario = Column(Text, nullable=False)
    
    resposta_ia = Column(Text, nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="registros_interacao_ia")
