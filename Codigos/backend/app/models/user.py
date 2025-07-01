"""
@file user.py
@brief Define o modelo SQLAlchemy principal para a tabela 'users' e a Base declarativa.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

import uuid
from sqlalchemy import (
    Column,
    String,
    Float,
    Date,
    Boolean,
    UUID,
)
from sqlalchemy.orm import declarative_base, relationship

# A Base declarativa é o ponto central para todos os nossos modelos.
# Todas as outras classes de modelo no projeto herdarão desta Base.
Base = declarative_base()

class User(Base):
    """
    Modelo de dados para a tabela 'users', representando um utilizador no sistema.

    Attributes:
        id (UUID): ID único do utilizador, gerado automaticamente.
        email (str): E-mail do utilizador, deve ser único e é indexado para buscas rápidas.
        hashed_password (str): A senha do utilizador, armazenada como um hash seguro.
        nome (str): Nome completo do utilizador.
        data_nascimento (Date): Data de nascimento do utilizador.
        altura_cm (float): Altura do utilizador em centímetros.
        peso_kg (float): Peso do utilizador em quilogramas.
        sexo (str): Sexo biológico ou género do utilizador.
        is_active (bool): Flag que indica se a conta do utilizador está ativa.
        is_superuser (bool): Flag que indica se o utilizador tem permissões de superadministrador.
        is_verified (bool): Flag que indica se o e-mail do utilizador foi verificado.
        registros_progresso (relationship): Relacionamento com os registos de progresso do utilizador.
        sessoes_de_treino (relationship): Relacionamento com as sessões de treino do utilizador.
        registros_interacao_ia (relationship): Relacionamento com as interações de IA do utilizador.
    """
    # Nome da tabela na base de dados.
    __tablename__ = "users"

    # --- Colunas Principais ---
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # --- Atributos do Perfil ---
    nome = Column(String, nullable=True)
    data_nascimento = Column(Date, nullable=True)
    altura_cm = Column(Float, nullable=True)
    peso_kg = Column(Float, nullable=True)
    sexo = Column(String, nullable=True)

    # --- Campos de Gestão da Conta ---
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # --- RELACIONAMENTOS ---
    registros_progresso = relationship(
        "RegistroProgresso",
        back_populates="owner",
        cascade="all, delete-orphan" # Apaga os registos se o utilizador for apagado.
    )

    sessoes_de_treino = relationship(
        "SessaoDeTreino", 
        back_populates="owner",
        cascade="all, delete-orphan" # Apaga as sessões se o utilizador for apagado.
    )

    registros_interacao_ia = relationship(
        "RegistroInteracaoIA", 
        back_populates="owner",
        cascade="all, delete-orphan" # Apaga as interações se o utilizador for apagado.
    )

    def __repr__(self):
        """Representação em string do objeto User, útil para depuração."""
        return f"<User(email='{self.email}')>"
