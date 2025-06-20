import uuid
from sqlalchemy import Column, String, Text, UUID
from sqlalchemy.orm import relationship

# Importamos a Base declarativa do nosso modelo de utilizador para manter tudo ligado.
from .user import Base

class Exercicio(Base):
    """
    Modelo para a tabela 'exercicios', como definido no diagrama de classes.
    Armazena os detalhes de cada exercício disponível na aplicação.
    """
    __tablename__ = "exercicios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(100), unique=True, nullable=False, index=True)
    descricao = Column(Text, nullable=True)
    instrucoes = Column(Text, nullable=True) # Este campo pode conter texto formatado com Markdown

    # Este relacionamento permite-nos ver todos os "ItemSessao" que se referem a este exercício.
    # Será ligado no próximo passo.
    itens_sessao = relationship("ItemSessao", back_populates="exercicio")
