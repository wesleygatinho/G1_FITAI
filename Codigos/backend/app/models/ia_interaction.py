import uuid
from sqlalchemy import Column, String, Text, ForeignKey, DateTime, UUID
from sqlalchemy.orm import relationship
from datetime import datetime

# Importamos a Base declarativa do nosso modelo de utilizador para manter tudo ligado.
from .user import Base

class RegistroInteracaoIA(Base):
    """
    Modelo para a tabela 'registro_interacao_ia', como definido no diagrama.
    Armazena o prompt do utilizador e a resposta gerada pela IA.
    """
    __tablename__ = "registro_interacao_ia"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # O prompt (pergunta) que o utilizador enviou.
    prompt_usuario = Column(Text, nullable=False)
    
    # A resposta que a IA gerou.
    resposta_ia = Column(Text, nullable=False)

    # Ligação ao utilizador que fez a pergunta.
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Relacionamento de volta para o utilizador.
    owner = relationship("User", back_populates="registros_interacao_ia")
