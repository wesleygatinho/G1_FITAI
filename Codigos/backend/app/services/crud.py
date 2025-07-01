"""
@file crud.py
@brief Contém todas as funções CRUD (Create, Read, Update, Delete) para interagir com a base de dados.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

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
    """Busca um utilizador pelo seu endereço de e-mail.

    :param (Session) db: A sessão da base de dados.
    :param (str) email: O e-mail do utilizador a ser procurado.
    :return (user_model.User | None): O objeto do utilizador ou None se não for encontrado.
    """
    return db.query(user_model.User).filter(user_model.User.email == email).first()

def create_user(db: Session, user: user_schema.UserCreate) -> user_model.User:
    """Cria um novo utilizador na base de dados.

    :param (Session) db: A sessão da base de dados.
    :param (user_schema.UserCreate) user: O objeto com os dados do utilizador a ser criado.
    :return (user_model.User): O objeto do utilizador recém-criado.
    """
    hashed_password = get_password_hash(user.password)
    db_user = user_model.User(email=user.email, hashed_password=hashed_password, nome=user.nome)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: user_model.User, user_in: user_schema.UserUpdate) -> user_model.User:
    """Atualiza os dados de um utilizador existente.

    :param (Session) db: A sessão da base de dados.
    :param (user_model.User) db_user: O objeto do utilizador a ser atualizado.
    :param (user_schema.UserUpdate) user_in: Os novos dados para o utilizador.
    :return (user_model.User): O objeto do utilizador atualizado.
    """
    user_data = user_in.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Funções CRUD de Progresso ---

def create_weight_record(db: Session, record: progress_schema.WeightRecordCreate, user_id: uuid.UUID) -> progress_model.WeightRecord:
    """Cria um novo registo de peso para um utilizador.

    :param (Session) db: A sessão da base de dados.
    :param (progress_schema.WeightRecordCreate) record: Os dados do registo de peso.
    :param (uuid.UUID) user_id: O ID do utilizador associado.
    :return (progress_model.WeightRecord): O registo de peso criado.
    """
    db_record = progress_model.WeightRecord(peso_kg=record.peso_kg, user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_weight_records_by_user(db: Session, user_id: uuid.UUID) -> List[progress_model.WeightRecord]:
    """Obtém todos os registos de peso de um utilizador, ordenados por data descendente.

    :param (Session) db: A sessão da base de dados.
    :param (uuid.UUID) user_id: O ID do utilizador.
    :return (List[progress_model.WeightRecord]): Uma lista de registos de peso.
    """
    return db.query(progress_model.WeightRecord).filter(progress_model.WeightRecord.user_id == user_id).order_by(desc(progress_model.WeightRecord.data)).all()

def create_body_measure_record(db: Session, record: progress_schema.BodyMeasureRecordCreate, user_id: uuid.UUID) -> progress_model.BodyMeasureRecord:
    """Cria um novo registo de medida corporal para um utilizador.

    :param (Session) db: A sessão da base de dados.
    :param (progress_schema.BodyMeasureRecordCreate) record: Os dados do registo de medida.
    :param (uuid.UUID) user_id: O ID do utilizador associado.
    :return (progress_model.BodyMeasureRecord): O registo de medida criado.
    """
    db_record = progress_model.BodyMeasureRecord(tipo_medida=record.tipo_medida, valor_cm=record.valor_cm, user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_body_measure_records_by_user(db: Session, user_id: uuid.UUID) -> List[progress_model.BodyMeasureRecord]:
    """Obtém todos os registos de medida corporal de um utilizador, ordenados por data.

    :param (Session) db: A sessão da base de dados.
    :param (uuid.UUID) user_id: O ID do utilizador.
    :return (List[progress_model.BodyMeasureRecord]): Uma lista de registos de medida corporal.
    """
    return db.query(progress_model.BodyMeasureRecord).filter(progress_model.BodyMeasureRecord.user_id == user_id).order_by(desc(progress_model.BodyMeasureRecord.data)).all()

def create_cardio_record(db: Session, record: progress_schema.CardioRecordCreate, user_id: uuid.UUID) -> progress_model.CardioRecord:
    """Cria um novo registo de exercício cardiovascular para um utilizador.

    :param (Session) db: A sessão da base de dados.
    :param (progress_schema.CardioRecordCreate) record: Os dados do registo de cardio.
    :param (uuid.UUID) user_id: O ID do utilizador associado.
    :return (progress_model.CardioRecord): O registo de cardio criado.
    """
    db_record = progress_model.CardioRecord(tempo_min=record.tempo_min, tipo_equipamento=record.tipo_equipamento, distancia_km=record.distancia_km, calorias=record.calorias, user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_cardio_records_by_user(db: Session, user_id: uuid.UUID) -> List[progress_model.CardioRecord]:
    """Obtém todos os registos de cardio de um utilizador, ordenados por data.

    :param (Session) db: A sessão da base de dados.
    :param (uuid.UUID) user_id: O ID do utilizador.
    :return (List[progress_model.CardioRecord]): Uma lista de registos de cardio.
    """
    return db.query(progress_model.CardioRecord).filter(progress_model.CardioRecord.user_id == user_id).order_by(desc(progress_model.CardioRecord.data)).all()

# --- Funções CRUD para Exercícios ---

def get_exercicio_by_nome(db: Session, nome: str) -> exercicio_model.Exercicio:
    """Busca um exercício pelo seu nome.

    :param (Session) db: A sessão da base de dados.
    :param (str) nome: O nome do exercício.
    :return (exercicio_model.Exercicio | None): O objeto do exercício ou None se não encontrado.
    """
    return db.query(exercicio_model.Exercicio).filter(exercicio_model.Exercicio.nome == nome).first()

def create_exercicio(db: Session, exercicio: exercicio_schema.ExercicioCreate) -> exercicio_model.Exercicio:
    """Cria um novo exercício na base de dados (usado para popular dados iniciais).

    :param (Session) db: A sessão da base de dados.
    :param (exercicio_schema.ExercicioCreate) exercicio: Os dados do exercício a ser criado.
    :return (exercicio_model.Exercicio): O exercício criado.
    """
    db_exercicio = exercicio_model.Exercicio(**exercicio.dict())
    db.add(db_exercicio)
    db.commit()
    db.refresh(db_exercicio)
    return db_exercicio

def get_exercicios(db: Session, skip: int = 0, limit: int = 100) -> List[exercicio_model.Exercicio]:
    """Obtém uma lista de todos os exercícios disponíveis, com paginação.

    :param (Session) db: A sessão da base de dados.
    :param (int) skip: O número de registos a pular.
    :param (int) limit: O número máximo de registos a retornar.
    :return (List[exercicio_model.Exercicio]): Uma lista de exercícios.
    """
    return db.query(exercicio_model.Exercicio).offset(skip).limit(limit).all()

# --- Funções CRUD de Sessão de Treino ---

def create_workout_session(db: Session, session_data: session_schema.SessaoDeTreinoCreate, user_id: uuid.UUID) -> session_model.SessaoDeTreino:
    """Cria uma nova sessão de treino com os seus itens associados.

    :param (Session) db: A sessão da base de dados.
    :param (session_schema.SessaoDeTreinoCreate) session_data: Os dados da sessão e seus itens.
    :param (uuid.UUID) user_id: O ID do utilizador que realizou a sessão.
    :return (session_model.SessaoDeTreino): A sessão de treino criada com seus itens.
    """
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
    """Obtém o histórico de sessões de treino de um utilizador.

    :param (Session) db: A sessão da base de dados.
    :param (uuid.UUID) user_id: O ID do utilizador.
    :param (int) skip: O número de sessões a pular.
    :param (int) limit: O número máximo de sessões a retornar.
    :return (List[session_model.SessaoDeTreino]): Uma lista de sessões de treino.
    """
    return db.query(session_model.SessaoDeTreino).filter(session_model.SessaoDeTreino.user_id == user_id).order_by(desc(session_model.SessaoDeTreino.data_inicio)).offset(skip).limit(limit).all()
    
# --- Funções CRUD para Interações com a IA ---

def create_ia_interaction(db: Session, interaction: ia_interaction_schema.RegistroInteracaoIACreate, user_id: uuid.UUID) -> ia_interaction_model.RegistroInteracaoIA:
    """Salva um registo de interação com a IA na base de dados.

    :param (Session) db: A sessão da base de dados.
    :param (ia_interaction_schema.RegistroInteracaoIACreate) interaction: Os dados da interação.
    :param (uuid.UUID) user_id: O ID do utilizador que interagiu com a IA.
    :return (ia_interaction_model.RegistroInteracaoIA): O registo da interação.
    """
    db_interaction = ia_interaction_model.RegistroInteracaoIA(prompt_usuario=interaction.prompt_usuario, resposta_ia=interaction.resposta_ia, user_id=user_id)
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

def get_ia_interactions_by_user(db: Session, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[ia_interaction_model.RegistroInteracaoIA]:
    """Obtém o histórico de interações de um utilizador com a IA.

    :param (Session) db: A sessão da base de dados.
    :param (uuid.UUID) user_id: O ID do utilizador.
    :param (int) skip: O número de interações a pular.
    :param (int) limit: O número máximo de interações a retornar.
    :return (List[ia_interaction_model.RegistroInteracaoIA]): Uma lista de interações.
    """
    return db.query(ia_interaction_model.RegistroInteracaoIA).filter(ia_interaction_model.RegistroInteracaoIA.user_id == user_id).order_by(desc(ia_interaction_model.RegistroInteracaoIA.data)).all()