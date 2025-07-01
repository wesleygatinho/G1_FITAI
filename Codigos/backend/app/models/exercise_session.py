"""
@file exercise_session.py
@brief Define os modelos SQLAlchemy para as tabelas 'sessoes_de_treino' e 'itens_sessao'.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, UUID, Text
from sqlalchemy.orm import relationship
from datetime import datetime

# Importa a Base declarativa a partir do módulo user para manter a ligação entre os modelos.
from .user import Base

class SessaoDeTreino(Base):
    """Modelo para a tabela 'sessoes_de_treino'.

    Representa uma sessão de treino completa de um utilizador, contendo
    um ou mais itens de sessão.

    Attributes:
        id (UUID): ID único da sessão de treino, gerado automaticamente.
        data_inicio (DateTime): Data e hora de início da sessão.
        data_fim (DateTime): Data e hora de fim da sessão, pode ser nula.
        user_id (UUID): Chave estrangeira que liga a sessão ao utilizador.
        owner (relationship): Relacionamento de volta para o utilizador.
        itens (relationship): Relacionamento com os itens da sessão.
    """
    __tablename__ = "sessoes_de_treino"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_inicio = Column(DateTime, default=datetime.utcnow)
    data_fim = Column(DateTime, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    owner = relationship("User", back_populates="sessoes_de_treino")
    
    # 'cascade="all, delete-orphan"' garante que os itens sejam apagados se a sessão for apagada.
    itens = relationship("ItemSessao", back_populates="sessao", cascade="all, delete-orphan")

class ItemSessao(Base):
    """Modelo para a tabela 'itens_sessao'.

    Representa um exercício específico dentro de uma sessão de treino.

    Attributes:
        id (UUID): ID único do item da sessão.
        series (int): Número de séries realizadas.
        repeticoes (int): Número de repetições realizadas.
        feedback_ia (Text): Feedback detalhado gerado pela IA sobre a execução.
        exercicio_id (UUID): Chave estrangeira para a tabela 'exercicios'.
        sessao_id (UUID): Chave estrangeira para a tabela 'sessoes_de_treino'.
        sessao (relationship): Relacionamento para aceder à sessão de treino pai.
        exercicio (relationship): Relacionamento para aceder ao exercício correspondente.
    """
    __tablename__ = "itens_sessao"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    series = Column(Integer)
    repeticoes = Column(Integer)
    feedback_ia = Column(Text, nullable=True)
    
    exercicio_id = Column(UUID(as_uuid=True), ForeignKey("exercicios.id"), nullable=False)
    sessao_id = Column(UUID(as_uuid=True), ForeignKey("sessoes_de_treino.id"), nullable=False)
    
    sessao = relationship("SessaoDeTreino", back_populates="itens")
    exercicio = relationship("Exercicio", back_populates="itens_sessao")
