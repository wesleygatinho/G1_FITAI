import uuid
from sqlalchemy import Column, String, Float, Date, Integer, ForeignKey, DateTime, UUID
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

# Importamos a Base declarativa do nosso modelo de utilizador para manter tudo ligado.
# Certifique-se de que no seu user.py a Base está definida assim: Base = declarative_base()
from .user import Base

class RegistroProgresso(Base):
    """
    Modelo base para todos os tipos de registos de progresso, como no diagrama.
    Usa a estratégia de herança "Joined Table".
    """
    __tablename__ = "registro_progresso"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Coluna "discriminadora" que diz ao SQLAlchemy qual o tipo de subclasse.
    type = Column(String(50))

    owner = relationship("User", back_populates="registros_progresso")

    __mapper_args__ = {
        "polymorphic_identity": "registro_progresso",
        "polymorphic_on": type,
    }

class WeightRecord(RegistroProgresso):
    """
    Modelo para Registos de Peso, herdando de RegistroProgresso.
    No diagrama, é 'RegistroPeso'.
    """
    __tablename__ = "registro_peso"
    
    id = Column(UUID(as_uuid=True), ForeignKey("registro_progresso.id"), primary_key=True)
    peso_kg = Column(Float, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "peso",
    }

class BodyMeasureRecord(RegistroProgresso):
    """
    Modelo para Registos de Medidas, herdando de RegistroProgresso.
    No diagrama, é 'RegistroMedida'.
    """
    __tablename__ = "registro_medida"
    
    id = Column(UUID(as_uuid=True), ForeignKey("registro_progresso.id"), primary_key=True)
    tipo_medida = Column(String, nullable=False) # Ex: "braço", "cintura"
    valor_cm = Column(Float, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "medida",
    }

class CardioRecord(RegistroProgresso):
    """
    Modelo para Registos de Cardio, herdando de RegistroProgresso.
    Agora inclui todos os campos do diagrama.
    """
    __tablename__ = "registro_cardio"
    
    id = Column(UUID(as_uuid=True), ForeignKey("registro_progresso.id"), primary_key=True)
    tipo_equipamento = Column(String, nullable=True) # Ex: "passadeira", "bicicleta"
    distancia_km = Column(Float, nullable=True)
    tempo_min = Column(Integer, nullable=False)
    calorias = Column(Integer, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "cardio",
    }

class RegistroImagemCorpo(RegistroProgresso):
    """
    Novo modelo para Registos de Imagem Corporal, como no diagrama.
    """
    __tablename__ = "registro_imagem_corpo"
    
    id = Column(UUID(as_uuid=True), ForeignKey("registro_progresso.id"), primary_key=True)
    endereco_imagem = Column(String, nullable=False)
    posicao = Column(String, nullable=True) # Ex: "frente", "lado"

    __mapper_args__ = {
        "polymorphic_identity": "imagem_corpo",
    }
