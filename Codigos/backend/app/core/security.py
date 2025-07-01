"""
@file security.py
@brief Fornece funções de utilidade para segurança, como hashing de senhas e criação de tokens JWT.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from .config import settings

# Contexto do Passlib para hashing e verificação de senhas.
# 'bcrypt' é o algoritmo recomendado pela sua robustez.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se uma senha em texto plano corresponde a um hash existente.

    :param (str) plain_password: A senha em texto plano a ser verificada.
    :param (str) hashed_password: O hash da senha armazenado na base de dados.
    :return (bool): True se a senha corresponder, False caso contrário.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera um hash seguro para uma senha em texto plano.

    :param (str) password: A senha em texto plano a ser processada.
    :return (str): O hash da senha gerado.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria um novo token de acesso JWT.

    Codifica os dados fornecidos num token JWT, adicionando um tempo de expiração.
    Se nenhum 'expires_delta' for fornecido, usa o tempo padrão das configurações.

    :param (dict) data: O payload (dados) a ser incluído no token. Deve conter o 'sub' (subject).
    :param (Optional[timedelta]) expires_delta: Tempo de vida opcional para o token.
    :return (str): O token de acesso JWT codificado como uma string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Usa o tempo de expiração padrão definido nas configurações da aplicação.
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
