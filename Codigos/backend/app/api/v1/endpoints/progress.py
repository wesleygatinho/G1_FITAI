from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import uuid

# --- IMPORTAÇÕES CORRIGIDAS ---
from app.models import user as user_model
from app.schemas import progress_record as progress_schema # Corrigido para o seu nome de ficheiro
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.services import crud

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
