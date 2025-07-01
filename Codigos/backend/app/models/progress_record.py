"""
@file progress_record.py
@brief Define os modelos SQLAlchemy para as tabelas de registo de progresso, utilizando herança polimórfica.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

import uuid
from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime, UUID
from sqlalchemy.orm import relationship
from datetime import datetime

# Importa a Base declarativa a partir do módulo user para manter a ligação entre os modelos.
from .user import Base

class RegistroProgresso(Base):
    """Modelo base para todos os tipos de registos de progresso.

    Usa a estratégia de herança "Joined Table" do SQLAlchemy para permitir
    diferentes tipos de registos partilhando campos comuns.

    Attributes:
        id (UUID): ID único para cada registo de progresso.
        data (DateTime): Data e hora do registo, preenchida com a data/hora atual por padrão.
        user_id (UUID): Chave estrangeira que liga o registo ao utilizador.
        type (str): Coluna "discriminadora" que armazena o tipo de subclasse (ex: "peso", "cardio").
        owner (relationship): Relacionamento para aceder ao objeto User a partir de um registo de progresso.
    """
    # Nome da tabela base na base de dados.
    __tablename__ = "registro_progresso"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    type = Column(String(50))

    owner = relationship("User", back_populates="registros_progresso")

    __mapper_args__ = {
        "polymorphic_identity": "registro_progresso",
        "polymorphic_on": type,
    }

class WeightRecord(RegistroProgresso):
    """Modelo para Registos de Peso, herdando de RegistroProgresso.

    Attributes:
        id (UUID): Chave primária que é também uma chave estrangeira para a tabela base.
        peso_kg (float): O valor do peso em quilogramas.
    """
    __tablename__ = "registro_peso"
    
    id = Column(UUID(as_uuid=True), ForeignKey("registro_progresso.id"), primary_key=True)
    peso_kg = Column(Float, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "peso",
    }

class BodyMeasureRecord(RegistroProgresso):
    """Modelo para Registos de Medidas Corporais, herdando de RegistroProgresso.

    Attributes:
        id (UUID): Chave primária que é também uma chave estrangeira para a tabela base.
        tipo_medida (str): O tipo de medida (ex: "braço", "cintura", "peito").
        valor_cm (float): O valor da medida em centímetros.
    """
    __tablename__ = "registro_medida"
    
    id = Column(UUID(as_uuid=True), ForeignKey("registro_progresso.id"), primary_key=True)
    tipo_medida = Column(String, nullable=False)
    valor_cm = Column(Float, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "medida",
    }

class CardioRecord(RegistroProgresso):
    """Modelo para Registos de Exercício Cardiovascular, herdando de RegistroProgresso.

    Attributes:
        id (UUID): Chave primária que é também uma chave estrangeira para a tabela base.
        tipo_equipamento (str): O tipo de equipamento utilizado (ex: "passadeira", "bicicleta").
        distancia_km (float): A distância percorrida em quilómetros.
        tempo_min (int): A duração do exercício em minutos.
        calorias (int): As calorias queimadas durante o exercício.
    """
    __tablename__ = "registro_cardio"
    
    id = Column(UUID(as_uuid=True), ForeignKey("registro_progresso.id"), primary_key=True)
    tipo_equipamento = Column(String, nullable=True)
    distancia_km = Column(Float, nullable=True)
    tempo_min = Column(Integer, nullable=False)
    calorias = Column(Integer, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "cardio",
    }

class RegistroImagemCorpo(RegistroProgresso):
    """Modelo para Registos de Imagem Corporal, herdando de RegistroProgresso.

    Attributes:
        id (UUID): Chave primária que é também uma chave estrangeira para a tabela base.
        endereco_imagem (str): URL ou caminho para o ficheiro da imagem armazenada.
        posicao (str): Posição da fotografia (ex: "frente", "lado", "costas").
    """
    __tablename__ = "registro_imagem_corpo"
    
    id = Column(UUID(as_uuid=True), ForeignKey("registro_progresso.id"), primary_key=True)
    endereco_imagem = Column(String, nullable=False)
    posicao = Column(String, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "imagem_corpo",
    }
