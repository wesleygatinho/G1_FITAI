import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel

# --- Schema Base (não usado diretamente, mas bom para referência) ---
class RegistroProgressoBase(BaseModel):
    data: Optional[datetime] = None

# --- Schemas para Peso ('RegistroPeso') ---
class WeightRecordBase(BaseModel):
    peso_kg: float

class WeightRecordCreate(WeightRecordBase):
    pass # Para criar, só precisamos do peso

class WeightRecord(WeightRecordBase):
    id: uuid.UUID
    data: datetime
    user_id: uuid.UUID

    class Config:
        from_attributes = True

# --- Schemas para Medidas ('RegistroMedida') ---
class BodyMeasureRecordBase(BaseModel):
    tipo_medida: str
    valor_cm: float

class BodyMeasureRecordCreate(BodyMeasureRecordBase):
    pass

class BodyMeasureRecord(BodyMeasureRecordBase):
    id: uuid.UUID
    data: datetime
    user_id: uuid.UUID
    
    class Config:
        from_attributes = True

# --- Schemas para Cardio ('RegistroCardio') ---
class CardioRecordBase(BaseModel):
    # Campos atualizados conforme o diagrama
    tempo_min: int
    tipo_equipamento: Optional[str] = None
    distancia_km: Optional[float] = None
    calorias: Optional[int] = None

class CardioRecordCreate(CardioRecordBase):
    pass

class CardioRecord(CardioRecordBase):
    id: uuid.UUID
    data: datetime
    user_id: uuid.UUID
    
    class Config:
        from_attributes = True

# --- Schemas para Imagem Corporal ('RegistroImagemCorpo') ---
class RegistroImagemCorpoBase(BaseModel):
    endereco_imagem: str
    posicao: Optional[str] = None

class RegistroImagemCorpoCreate(RegistroImagemCorpoBase):
    pass

class RegistroImagemCorpo(RegistroImagemCorpoBase):
    id: uuid.UUID
    data: datetime
    user_id: uuid.UUID

    class Config:
        from_attributes = True

# --- NOVOS SCHEMAS PARA OCR ---
class OcrRequest(BaseModel):
    image_base64: str
    data_type: str # 'weight', 'cardio', etc.

class OcrResponse(BaseModel):
    extracted_data: Dict[str, Any]