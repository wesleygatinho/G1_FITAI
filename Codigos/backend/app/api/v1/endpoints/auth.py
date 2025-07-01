"""
@file auth.py
@brief Define os endpoints da API para autenticação de utilizadores, incluindo registo, login e Google Sign-In.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# Importações de módulos da aplicação
from app.schemas.token import Token
from app.schemas.user import User, UserCreate
from app.services import crud
from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.core.config import settings

# Cria uma nova instância de roteador para os endpoints de autenticação.
router = APIRouter()

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Regista um novo utilizador com e-mail e senha.

    Verifica se o e-mail já existe na base de dados antes de criar um novo registo.

    :param (UserCreate) user: Os dados do novo utilizador a serem criados.
    :param (Session) db: A sessão da base de dados.
    :raises HTTPException: Se o e-mail fornecido já estiver registado.
    :return (User): Os dados do utilizador recém-criado (sem a senha).
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
    """Autentica um utilizador com e-mail e senha, retornando um token de acesso JWT.

    :param (Session) db: A sessão da base de dados.
    :param (OAuth2PasswordRequestForm) form_data: Dados do formulário com 'username' (e-mail) e 'password'.
    :raises HTTPException: Se o e-mail ou a senha estiverem incorretos.
    :return (Token): O token de acesso e o seu tipo ("bearer").
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
    """Schema para a requisição de login com o token do Google.

    Attributes:
        token (str): O ID Token fornecido pelo Google Sign-In no cliente (Flutter).
    """
    token: str

@router.post("/google/token", response_model=Token)
def login_with_google_token(google_token: GoogleToken, db: Session = Depends(get_db)):
    """Autentica ou regista um utilizador usando um ID Token do Google.

    Valida o token do Google, verifica se o utilizador existe na base de dados local,
    cria um novo utilizador se necessário, e emite um token JWT da nossa própria API.

    :param (GoogleToken) google_token: O corpo da requisição contendo o token do Google.
    :param (Session) db: A sessão da base de dados.
    :raises HTTPException: Se o token do Google for inválido.
    :return (Token): O token de acesso da nossa API e o seu tipo ("bearer").
    """
    try:
        # Valida o token recebido junto aos servidores do Google.
        idinfo = id_token.verify_oauth2_token(
            google_token.token, 
            google_requests.Request(), 
            settings.GOOGLE_CLIENT_ID
        )

        email = idinfo['email']
        nome = idinfo.get('name', 'Usuário Google')

        # Verifica se o utilizador já existe no nosso sistema.
        db_user = crud.get_user_by_email(db, email=email)

        # Se não existir, cria um novo utilizador.
        if not db_user:
            new_user_data = UserCreate(
                email=email,
                nome=nome,
                # Gera uma senha segura a partir do ID único do Google (sub).
                # Esta senha não é usada para login direto.
                password=idinfo.get('sub')
            )
            db_user = crud.create_user(db=db, user=new_user_data)

        # Gera o nosso próprio token de acesso (JWT) para o utilizador.
        access_token = create_access_token(data={"sub": db_user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    except ValueError as e:
        # Ocorre se o token do Google for inválido ou expirado.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token do Google inválido: {e}",
        )
