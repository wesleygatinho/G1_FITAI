from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ....schemas.token import Token
from ....schemas.user import User, UserCreate
from ....services import crud
from ....core.database import get_db
from ....core.security import create_access_token, verify_password
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from ....core.config import settings


router = APIRouter()

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint para registrar um novo usuário.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado",
        )
    return crud.create_user(db=db, user=user)

@router.post("/login", response_model=Token)
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Endpoint para login. Recebe email (como username) e senha.
    Retorna um token de acesso JWT.
    """
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}


class GoogleToken(BaseModel):
    token: str

@router.post("/google/token", response_model=Token)
def login_with_google_token(google_token: GoogleToken, db: Session = Depends(get_db)):
    """
    Recebe um ID Token do Google Sign-In (vindo do Flutter),
    valida-o, e então loga ou registra o usuário.
    """
    try:
        # Valida o token recebido
        idinfo = id_token.verify_oauth2_token(
            google_token.token, 
            google_requests.Request(), 
            settings.GOOGLE_CLIENT_ID # O ID de cliente do tipo "Web"
        )

        email = idinfo['email']
        nome = idinfo.get('name', 'Usuário Google')

        # Verifica se o usuário já existe no nosso banco de dados
        db_user = crud.get_user_by_email(db, email=email)

        # Se não existir, cria um novo
        if not db_user:
            new_user_data = UserCreate(
                email=email,
                nome=nome,
                # A senha não será usada para login, então geramos uma a partir do sub (ID do Google)
                password=idinfo.get('sub')
            )
            db_user = crud.create_user(db=db, user=new_user_data)

        # Gera o nosso próprio token de acesso (JWT) para o usuário
        access_token = create_access_token(data={"sub": db_user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    except ValueError as e:
        # O token é inválido
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token do Google inválido: {e}",
        )