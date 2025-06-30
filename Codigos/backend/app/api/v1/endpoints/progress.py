from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any, Dict
import uuid

# --- IMPORTAÇÕES CORRIGIDAS ---
from app.models import user as user_model
from app.schemas import progress_record as progress_schema
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.services import crud
from app.services.ai_generation_service import ai_generation_service

router = APIRouter()

# --- Endpoints para Peso ('RegistroPeso') ---
@router.post("/weight", response_model=progress_schema.WeightRecord, status_code=201)
def add_weight_record(record: progress_schema.WeightRecordCreate, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_active_user)):
    return crud.create_weight_record(db=db, record=record, user_id=current_user.id)

@router.get("/weight", response_model=List[progress_schema.WeightRecord])
def read_weight_records(db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_active_user)):
    return crud.get_weight_records_by_user(db, user_id=current_user.id)

# --- Endpoints para Medidas ('RegistroMedida') ---
@router.post("/measure", response_model=progress_schema.BodyMeasureRecord, status_code=201)
def add_body_measure_record(record: progress_schema.BodyMeasureRecordCreate, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_active_user)):
    return crud.create_body_measure_record(db=db, record=record, user_id=current_user.id)

@router.get("/measure", response_model=List[progress_schema.BodyMeasureRecord])
def read_body_measure_records(db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_active_user)):
    return crud.get_body_measure_records_by_user(db, user_id=current_user.id)

# --- Endpoints para Cardio ('RegistroCardio') ---
@router.post("/cardio", response_model=progress_schema.CardioRecord, status_code=201)
def add_cardio_record(record: progress_schema.CardioRecordCreate, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_active_user)):
    return crud.create_cardio_record(db=db, record=record, user_id=current_user.id)

@router.get("/cardio", response_model=List[progress_schema.CardioRecord])
def read_cardio_records(db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_active_user)):
    return crud.get_cardio_records_by_user(db, user_id=current_user.id)

# --- NOVO ENDPOINT DE OCR ---
@router.post("/ocr/extract", response_model=progress_schema.OcrResponse, status_code=status.HTTP_200_OK)
def extract_data_from_image(
    request: progress_schema.OcrRequest,
    current_user: user_model.User = Depends(get_current_active_user)
):
    """
    Recebe uma imagem em base64 e o tipo de dado a ser extraído,
    e retorna os dados extraídos pela IA.
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