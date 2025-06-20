from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import desc
import uuid

from app.models import user as user_model
from app.models import progress_record as progress_model
from app.models import exercicio as exercicio_model
from app.models import exercise_session as session_model
from app.models import ia_interaction as ia_interaction_model
from app.schemas import user as user_schema
from app.schemas import progress_record as progress_schema
from app.schemas import exercicio as exercicio_schema
from app.schemas import exercise_session as session_schema
from app.schemas import ia_interaction as ia_interaction_schema
from app.core.security import get_password_hash

# --- Funções CRUD de Utilizador ---
def get_user_by_email(db: Session, email: str) -> user_model.User:
    return db.query(user_model.User).filter(user_model.User.email == email).first()

def create_user(db: Session, user: user_schema.UserCreate) -> user_model.User:
    hashed_password = get_password_hash(user.password)
    db_user = user_model.User(email=user.email, hashed_password=hashed_password, nome=user.nome)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: user_model.User, user_in: user_schema.UserUpdate) -> user_model.User:
    user_data = user_in.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Funções CRUD de Progresso ---

def create_weight_record(db: Session, record: progress_schema.WeightRecordCreate, user_id: uuid.UUID) -> progress_model.WeightRecord:
    db_record = progress_model.WeightRecord(peso_kg=record.peso_kg, user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_weight_records_by_user(db: Session, user_id: uuid.UUID) -> List[progress_model.WeightRecord]:
    return db.query(progress_model.WeightRecord).filter(progress_model.WeightRecord.user_id == user_id).order_by(desc(progress_model.WeightRecord.data)).all()

def create_body_measure_record(db: Session, record: progress_schema.BodyMeasureRecordCreate, user_id: uuid.UUID) -> progress_model.BodyMeasureRecord:
    db_record = progress_model.BodyMeasureRecord(tipo_medida=record.tipo_medida, valor_cm=record.valor_cm, user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_body_measure_records_by_user(db: Session, user_id: uuid.UUID) -> List[progress_model.BodyMeasureRecord]:
    return db.query(progress_model.BodyMeasureRecord).filter(progress_model.BodyMeasureRecord.user_id == user_id).order_by(desc(progress_model.BodyMeasureRecord.data)).all()

def create_cardio_record(db: Session, record: progress_schema.CardioRecordCreate, user_id: uuid.UUID) -> progress_model.CardioRecord:
    db_record = progress_model.CardioRecord(tempo_min=record.tempo_min, tipo_equipamento=record.tipo_equipamento, distancia_km=record.distancia_km, calorias=record.calorias, user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_cardio_records_by_user(db: Session, user_id: uuid.UUID) -> List[progress_model.CardioRecord]:
    return db.query(progress_model.CardioRecord).filter(progress_model.CardioRecord.user_id == user_id).order_by(desc(progress_model.CardioRecord.data)).all()

# --- Funções CRUD para Exercícios ---

def get_exercicio_by_nome(db: Session, nome: str) -> exercicio_model.Exercicio:
    return db.query(exercicio_model.Exercicio).filter(exercicio_model.Exercicio.nome == nome).first()

def create_exercicio(db: Session, exercicio: exercicio_schema.ExercicioCreate) -> exercicio_model.Exercicio:
    db_exercicio = exercicio_model.Exercicio(**exercicio.dict())
    db.add(db_exercicio)
    db.commit()
    db.refresh(db_exercicio)
    return db_exercicio

def get_exercicios(db: Session, skip: int = 0, limit: int = 100) -> List[exercicio_model.Exercicio]:
    return db.query(exercicio_model.Exercicio).offset(skip).limit(limit).all()

# --- Funções CRUD de Sessão de Treino ---

def create_workout_session(db: Session, session_data: session_schema.SessaoDeTreinoCreate, user_id: uuid.UUID) -> session_model.SessaoDeTreino:
    db_session = session_model.SessaoDeTreino(user_id=user_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    for item_data in session_data.itens:
        db_item = session_model.ItemSessao(**item_data.dict(), sessao_id=db_session.id)
        db.add(db_item)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_sessions_by_user(db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[session_model.SessaoDeTreino]:
    return db.query(session_model.SessaoDeTreino).filter(session_model.SessaoDeTreino.user_id == user_id).order_by(desc(session_model.SessaoDeTreino.data_inicio)).offset(skip).limit(limit).all()
    
# --- Funções CRUD para Interações com a IA ---

def create_ia_interaction(db: Session, interaction: ia_interaction_schema.RegistroInteracaoIACreate, user_id: uuid.UUID) -> ia_interaction_model.RegistroInteracaoIA:
    db_interaction = ia_interaction_model.RegistroInteracaoIA(prompt_usuario=interaction.prompt_usuario, resposta_ia=interaction.resposta_ia, user_id=user_id)
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

def get_ia_interactions_by_user(db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[ia_interaction_model.RegistroInteracaoIA]:
    return db.query(ia_interaction_model.RegistroInteracaoIA).filter(ia_interaction_model.RegistroInteracaoIA.user_id == user_id).order_by(desc(ia_interaction_model.RegistroInteracaoIA.data)).all()