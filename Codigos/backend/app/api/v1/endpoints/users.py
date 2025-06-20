from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.user import User as UserModel
from app.schemas.user import User, UserUpdate
from app.core.dependencies import get_current_active_user
from app.services import crud
from app.core.database import get_db

router = APIRouter()

@router.get("/me", response_model=User)
def read_user_me(current_user: UserModel = Depends(get_current_active_user)):
    """
    Recupera os dados do utilizador autenticado.
    """
    return current_user

@router.put("/me", response_model=User)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: UserModel = Depends(get_current_active_user)
):
    """
    Atualiza os dados do utilizador autenticado.
    """
    user = crud.update_user(db, db_user=current_user, user_in=user_in)
    return user
