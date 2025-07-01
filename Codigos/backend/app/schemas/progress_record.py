"""
@file progress_record.py
@brief Define os schemas Pydantic para as diferentes entidades de registo de progresso.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel

class RegistroProgressoBase(BaseModel):
    """Schema base de referência para todos os registos de progresso.

    Attributes:
        data (Optional[datetime]): Data do registo, opcional pois é gerada automaticamente na criação.
    """
    data: Optional[datetime] = None

# --- Schemas para Peso ('WeightRecord') ---

class WeightRecordBase(BaseModel):
    """Schema base para um registo de peso.

    Attributes:
        peso_kg (float): O peso registado em quilogramas.
    """
    peso_kg: float

class WeightRecordCreate(WeightRecordBase):
    """Schema para validar dados ao criar um novo registo de peso."""
    pass

class WeightRecord(WeightRecordBase):
    """Schema para representar um registo de peso lido da base de dados.

    Attributes:
        id (uuid.UUID): ID único do registo.
        data (datetime): Data e hora do registo.
        user_id (uuid.UUID): ID do utilizador associado ao registo.
    """
    id: uuid.UUID
    data: datetime
    user_id: uuid.UUID

    class Config:
        """Configuração Pydantic para mapeamento ORM."""
        from_attributes = True

# --- Schemas para Medidas Corporais ('BodyMeasureRecord') ---

class BodyMeasureRecordBase(BaseModel):
    """Schema base para um registo de medida corporal.

    Attributes:
        tipo_medida (str): O tipo de medida (ex: "cintura", "braço direito").
        valor_cm (float): O valor da medida em centímetros.
    """
    tipo_medida: str
    valor_cm: float

class BodyMeasureRecordCreate(BodyMeasureRecordBase):
    """Schema para validar dados ao criar um novo registo de medida corporal."""
    pass

class BodyMeasureRecord(BodyMeasureRecordBase):
    """Schema para representar um registo de medida corporal lido da base de dados.

    Attributes:
        id (uuid.UUID): ID único do registo.
        data (datetime): Data e hora do registo.
        user_id (uuid.UUID): ID do utilizador associado.
    """
    id: uuid.UUID
    data: datetime
    user_id: uuid.UUID
    
    class Config:
        """Configuração Pydantic para mapeamento ORM."""
        from_attributes = True

# --- Schemas para Exercício Cardiovascular ('CardioRecord') ---

class CardioRecordBase(BaseModel):
    """Schema base para um registo de exercício cardiovascular.

    Attributes:
        tempo_min (int): Duração do exercício em minutos.
        tipo_equipamento (Optional[str]): Tipo de equipamento (ex: "esteira", "bicicleta").
        distancia_km (Optional[float]): Distância percorrida em quilómetros.
        calorias (Optional[int]): Calorias queimadas.
    """
    tempo_min: int
    tipo_equipamento: Optional[str] = None
    distancia_km: Optional[float] = None
    calorias: Optional[int] = None

class CardioRecordCreate(CardioRecordBase):
    """Schema para validar dados ao criar um novo registo de cardio."""
    pass

class CardioRecord(CardioRecordBase):
    """Schema para representar um registo de cardio lido da base de dados.

    Attributes:
        id (uuid.UUID): ID único do registo.
        data (datetime): Data e hora do registo.
        user_id (uuid.UUID): ID do utilizador associado.
    """
    id: uuid.UUID
    data: datetime
    user_id: uuid.UUID
    
    class Config:
        """Configuração Pydantic para mapeamento ORM."""
        from_attributes = True

# --- Schemas para Imagem Corporal ('BodyImageRecord') ---

class BodyImageRecordBase(BaseModel):
    """Schema base para um registo de imagem corporal.

    Attributes:
        endereco_imagem (str): URL ou caminho para a imagem armazenada.
        posicao (Optional[str]): Posição da foto (ex: "frente", "lado", "costas").
    """
    endereco_imagem: str
    posicao: Optional[str] = None

class BodyImageRecordCreate(BodyImageRecordBase):
    """Schema para validar dados ao criar um novo registo de imagem corporal."""
    pass

class BodyImageRecord(BodyImageRecordBase):
    """Schema para representar um registo de imagem corporal lido da base de dados.

    Attributes:
        id (uuid.UUID): ID único do registo.
        data (datetime): Data e hora do registo.
        user_id (uuid.UUID): ID do utilizador associado.
    """
    id: uuid.UUID
    data: datetime
    user_id: uuid.UUID

    class Config:
        """Configuração Pydantic para mapeamento ORM."""
        from_attributes = True

# --- Schemas para Requisição e Resposta de OCR ---

class OcrRequest(BaseModel):
    """Schema para a requisição de extração de dados por OCR a partir de uma imagem.

    Attributes:
        image_base64 (str): A imagem codificada em formato base64.
        data_type (str): O tipo de dado a ser extraído (ex: 'weight', 'cardio').
    """
    image_base64: str
    data_type: str

class OcrResponse(BaseModel):
    """Schema para a resposta da extração de dados por OCR.

    Attributes:
        extracted_data (Dict[str, Any]): Dicionário contendo os dados extraídos pela IA.
    """
    extracted_data: Dict[str, Any]
