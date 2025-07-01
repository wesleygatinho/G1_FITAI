"""
@file token.py
@brief Define os schemas Pydantic para os tokens de autenticação JWT.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """Representa a estrutura do token de acesso que é retornado ao utilizador após o login.

    Attributes:
        access_token (str): O token de acesso JWT gerado.
        token_type (str): O tipo do token, geralmente "bearer".
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Representa os dados (payload) codificados dentro de um token JWT.

    Este schema é usado para validar o conteúdo do token após a sua decodificação.

    Attributes:
        email (Optional[str]): O e-mail do utilizador, que serve como identificador (subject) no token.
    """
    email: Optional[str] = None
