"""
@file exercicio.py
@brief Define o modelo SQLAlchemy para a tabela 'exercicios'.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

import uuid
from sqlalchemy import Column, String, Text, UUID
from sqlalchemy.orm import relationship

# Importa a Base declarativa a partir do módulo user para manter a ligação entre os modelos.
from .user import Base

class Exercicio(Base):
    """Modelo para a tabela 'exercicios'.

    Armazena os detalhes de cada exercício disponível na aplicação,
    como nome, descrição e instruções de execução.

    Attributes:
        id (UUID): ID único do exercício, gerado automaticamente.
        nome (str): Nome do exercício, deve ser único e é indexado.
        descricao (Text): Descrição textual do exercício.
        instrucoes (Text): Instruções detalhadas de como realizar o exercício.
        itens_sessao (relationship): Relacionamento com os itens de sessão associados.
    """
    # Nome da tabela na base de dados.
    __tablename__ = "exercicios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(100), unique=True, nullable=False, index=True)
    descricao = Column(Text, nullable=True)
    instrucoes = Column(Text, nullable=True)

    # 'back_populates' cria a ligação inversa no modelo 'ItemSessao'.
    itens_sessao = relationship("ItemSessao", back_populates="exercicio")
