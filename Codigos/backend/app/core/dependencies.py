"""
@file dependencies.py
@brief Define as dependências da API para autenticação e autorização de utilizadores.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.services import crud
from app.schemas.token import TokenData
from app.models.user import User
from app.core.config import settings
from app.core.database import get_db

# Cria uma instância do esquema de autenticação OAuth2.
# 'tokenUrl' aponta para o endpoint de login onde o token é obtido.
# FastAPI usará isso para extrair o token do cabeçalho 'Authorization'.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """Decodifica o token JWT para obter o utilizador atual da base de dados.

    Esta função é uma dependência que:
    1. Extrai o token JWT da requisição.
    2. Decodifica e valida o token.
    3. Extrai o e-mail (subject) do payload do token.
    4. Busca o utilizador na base de dados com base no e-mail.

    :param (Session) db: A sessão da base de dados, injetada por `get_db`.
    :param (str) token: O token JWT, injetado por `oauth2_scheme`.
    :raises HTTPException: Se o token for inválido, malformado ou o utilizador não existir.
    :return (User): O modelo SQLAlchemy do utilizador autenticado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Obtém o utilizador autenticado e verifica se ele está ativo.

    Esta é a dependência principal para proteger endpoints. Ela primeiro obtém
    o utilizador com `get_current_user` e depois verifica a flag `is_active`.

    :param (User) current_user: O utilizador, injetado pela dependência `get_current_user`.
    :raises HTTPException: Se a conta do utilizador estiver inativa.
    :return (User): O modelo SQLAlchemy do utilizador ativo e autenticado.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Utilizador inativo")
    return current_user
