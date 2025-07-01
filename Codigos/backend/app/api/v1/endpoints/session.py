"""
@file session.py
@brief Define os endpoints da API para a gestão de sessões de treino do utilizador.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.user import User as UserModel
from app.schemas.exercise_session import SessaoDeTreino, SessaoDeTreinoCreate
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.services import crud

# Cria uma nova instância de roteador para os endpoints de sessão de treino.
router = APIRouter()

@router.get("/", response_model=List[SessaoDeTreino])
def read_workout_sessions(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 25,
    current_user: UserModel = Depends(get_current_active_user)
):
    """Recupera o histórico paginado de sessões de treino para o utilizador autenticado.

    :param (Session) db: A sessão da base de dados.
    :param (int) skip: O número de sessões a pular (para paginação).
    :param (int) limit: O número máximo de sessões a retornar.
    :param (UserModel) current_user: O utilizador autenticado.
    :return (List[SessaoDeTreino]): Uma lista de objetos de sessão de treino.
    """
    sessions = crud.get_sessions_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return sessions


@router.post("/", response_model=SessaoDeTreino, status_code=status.HTTP_201_CREATED)
def create_workout_session(
    *,
    db: Session = Depends(get_db),
    session_in: SessaoDeTreinoCreate,
    current_user: UserModel = Depends(get_current_active_user)
):
    """Cria uma nova sessão de treino para o utilizador autenticado.

    Recebe uma lista de exercícios realizados (itens da sessão) e os persiste na base de dados.

    :param (Session) db: A sessão da base de dados.
    :param (SessaoDeTreinoCreate) session_in: Os dados da sessão a ser criada, incluindo seus itens.
    :param (UserModel) current_user: O utilizador autenticado.
    :raises HTTPException: Se a sessão de treino não contiver nenhum item.
    :return (SessaoDeTreino): A sessão de treino recém-criada.
    """
    if not session_in.itens:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível guardar uma sessão de treino vazia."
        )
    session = crud.create_workout_session(db=db, session_data=session_in, user_id=current_user.id)
    return session
