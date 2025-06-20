import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, UUID, Text
from sqlalchemy.orm import relationship
from datetime import datetime

# Importamos a Base do user.py para manter a consistência
from .user import Base

class SessaoDeTreino(Base):
    """
    Modelo para a tabela 'sessoes_de_treino', como no diagrama.
    Representa uma sessão de treino completa de um utilizador.
    """
    __tablename__ = "sessoes_de_treino"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_inicio = Column(DateTime, default=datetime.utcnow)
    data_fim = Column(DateTime, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Relação de volta para o utilizador
    owner = relationship("User", back_populates="sessoes_de_treino")
    
    # Relação com os itens da sessão
    itens = relationship("ItemSessao", back_populates="sessao", cascade="all, delete-orphan")

class ItemSessao(Base):
    """
    Modelo para a tabela 'itens_sessao', como no diagrama.
    Representa um exercício específico dentro de uma sessão de treino.
    """
    __tablename__ = "itens_sessao"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    series = Column(Integer)
    repeticoes = Column(Integer)
    feedback_ia = Column(Text, nullable=True) # Alterado para Text para mais detalhes
    
    # --- ALTERAÇÃO PRINCIPAL ---
    # Substituímos o nome do exercício por uma ligação direta à tabela 'exercicios'
    exercicio_id = Column(UUID(as_uuid=True), ForeignKey("exercicios.id"), nullable=False)
    
    sessao_id = Column(UUID(as_uuid=True), ForeignKey("sessoes_de_treino.id"), nullable=False)
    
    # Relações
    sessao = relationship("SessaoDeTreino", back_populates="itens")
    exercicio = relationship("Exercicio", back_populates="itens_sessao")
