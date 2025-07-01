"""
@file users.py
@brief Define os endpoints da API para a gestão do perfil do utilizador autenticado.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.user import User as UserModel
from app.schemas.user import User, UserUpdate
from app.core.dependencies import get_current_active_user
from app.services import crud
from app.core.database import get_db

# Cria uma nova instância de roteador para os endpoints de utilizador.
router = APIRouter()

@router.get("/me", response_model=User)
def read_user_me(current_user: UserModel = Depends(get_current_active_user)):
    """Recupera os dados do perfil do utilizador atualmente autenticado.

    :param (UserModel) current_user: O utilizador autenticado, injetado pela dependência.
    :return (User): O objeto do utilizador com os seus dados de perfil.
    """
    return current_user

@router.put("/me", response_model=User)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: UserModel = Depends(get_current_active_user)
):
    """Atualiza os dados do perfil do utilizador atualmente autenticado.

    :param (Session) db: A sessão da base de dados.
    :param (UserUpdate) user_in: Os novos dados a serem atualizados para o utilizador.
    :param (UserModel) current_user: O utilizador autenticado a ser atualizado.
    :return (User): O objeto do utilizador com os dados atualizados.
    """
    user = crud.update_user(db, db_user=current_user, user_in=user_in)
    return user
