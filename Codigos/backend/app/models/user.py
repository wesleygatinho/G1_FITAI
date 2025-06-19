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
Base = declarative_base()

class User(Base):
    """
    Modelo de dados para a tabela 'users', atualizado para
    corresponder ao novo diagrama de classes.
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Atributos do perfil do utilizador, conforme o diagrama
    nome = Column(String, nullable=True)
    data_nascimento = Column(Date, nullable=True)
    altura_cm = Column(Float, nullable=True)
    peso_kg = Column(Float, nullable=True)
    sexo = Column(String, nullable=True)

    # Campos de gestão da conta
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # --- RELACIONAMENTOS FINAIS ---
    registros_progresso = relationship(
        "RegistroProgresso",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    sessoes_de_treino = relationship(
        "SessaoDeTreino", 
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    # Relacionamento com as interações de IA, agora ativo
    registros_interacao_ia = relationship(
        "RegistroInteracaoIA", 
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(email='{self.email}')>"