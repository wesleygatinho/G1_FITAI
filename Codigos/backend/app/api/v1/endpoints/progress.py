"""
@file progress.py
@brief Define os endpoints da API para a gestão de registos de progresso do utilizador.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any, Dict
import uuid

# Importações dos módulos da aplicação
from app.models import user as user_model
from app.schemas import progress_record as progress_schema
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.services import crud
from app.services.ai_generation_service import ai_generation_service

# Cria uma nova instância de roteador para os endpoints de progresso.
router = APIRouter()

# --- Endpoints para Peso ('WeightRecord') ---

@router.post("/weight", response_model=progress_schema.WeightRecord, status_code=201)
def add_weight_record(
    record: progress_schema.WeightRecordCreate, 
    db: Session = Depends(get_db), 
    current_user: user_model.User = Depends(get_current_active_user)
):
    """Adiciona um novo registo de peso para o utilizador autenticado.

    :param (progress_schema.WeightRecordCreate) record: Os dados do registo de peso a criar.
    :param (Session) db: A sessão da base de dados.
    :param (user_model.User) current_user: O utilizador autenticado.
    :return (progress_schema.WeightRecord): O registo de peso criado.
    """
    return crud.create_weight_record(db=db, record=record, user_id=current_user.id)

@router.get("/weight", response_model=List[progress_schema.WeightRecord])
def read_weight_records(
    db: Session = Depends(get_db), 
    current_user: user_model.User = Depends(get_current_active_user)
):
    """Obtém o histórico de registos de peso do utilizador autenticado.

    :param (Session) db: A sessão da base de dados.
    :param (user_model.User) current_user: O utilizador autenticado.
    :return (List[progress_schema.WeightRecord]): Uma lista de registos de peso.
    """
    return crud.get_weight_records_by_user(db, user_id=current_user.id)

# --- Endpoints para Medidas ('BodyMeasureRecord') ---

@router.post("/measure", response_model=progress_schema.BodyMeasureRecord, status_code=201)
def add_body_measure_record(
    record: progress_schema.BodyMeasureRecordCreate, 
    db: Session = Depends(get_db), 
    current_user: user_model.User = Depends(get_current_active_user)
):
    """Adiciona um novo registo de medida corporal para o utilizador autenticado.

    :param (progress_schema.BodyMeasureRecordCreate) record: Os dados da medida a criar.
    :param (Session) db: A sessão da base de dados.
    :param (user_model.User) current_user: O utilizador autenticado.
    :return (progress_schema.BodyMeasureRecord): O registo de medida criado.
    """
    return crud.create_body_measure_record(db=db, record=record, user_id=current_user.id)

@router.get("/measure", response_model=List[progress_schema.BodyMeasureRecord])
def read_body_measure_records(
    db: Session = Depends(get_db), 
    current_user: user_model.User = Depends(get_current_active_user)
):
    """Obtém o histórico de registos de medidas corporais do utilizador autenticado.

    :param (Session) db: A sessão da base de dados.
    :param (user_model.User) current_user: O utilizador autenticado.
    :return (List[progress_schema.BodyMeasureRecord]): Uma lista de registos de medida.
    """
    return crud.get_body_measure_records_by_user(db, user_id=current_user.id)

# --- Endpoints para Cardio ('CardioRecord') ---

@router.post("/cardio", response_model=progress_schema.CardioRecord, status_code=201)
def add_cardio_record(
    record: progress_schema.CardioRecordCreate, 
    db: Session = Depends(get_db), 
    current_user: user_model.User = Depends(get_current_active_user)
):
    """Adiciona um novo registo de exercício cardiovascular para o utilizador autenticado.

    :param (progress_schema.CardioRecordCreate) record: Os dados do registo de cardio a criar.
    :param (Session) db: A sessão da base de dados.
    :param (user_model.User) current_user: O utilizador autenticado.
    :return (progress_schema.CardioRecord): O registo de cardio criado.
    """
    return crud.create_cardio_record(db=db, record=record, user_id=current_user.id)

@router.get("/cardio", response_model=List[progress_schema.CardioRecord])
def read_cardio_records(
    db: Session = Depends(get_db), 
    current_user: user_model.User = Depends(get_current_active_user)
):
    """Obtém o histórico de registos de cardio do utilizador autenticado.

    :param (Session) db: A sessão da base de dados.
    :param (user_model.User) current_user: O utilizador autenticado.
    :return (List[progress_schema.CardioRecord]): Uma lista de registos de cardio.
    """
    return crud.get_cardio_records_by_user(db, user_id=current_user.id)

# --- Endpoint de OCR ---

@router.post("/ocr/extract", response_model=progress_schema.OcrResponse, status_code=status.HTTP_200_OK)
def extract_data_from_image(
    request: progress_schema.OcrRequest,
    current_user: user_model.User = Depends(get_current_active_user)
):
    """Extrai dados de uma imagem usando o serviço de OCR da IA.

    Recebe uma imagem em base64 e um tipo de dado ('weight', 'cardio'),
    e retorna os dados estruturados extraídos pela IA.

    :param (progress_schema.OcrRequest) request: O corpo da requisição com a imagem e o tipo de dado.
    :param (user_model.User) current_user: O utilizador autenticado.
    :raises HTTPException: Se o serviço de IA retornar um erro.
    :return (progress_schema.OcrResponse): Um dicionário com os dados extraídos.
    """
    extracted_data = ai_generation_service.extract_data_from_image_with_gemini(
        image_base64=request.image_base64,
        data_type=request.data_type
    )
    
    if "error" in extracted_data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=extracted_data["error"]
        )
        
    return {"extracted_data": extracted_data}
