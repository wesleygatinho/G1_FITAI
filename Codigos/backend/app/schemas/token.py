from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """
    Schema para o token de acesso JWT.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema para os dados contidos dentro do token JWT.
    """
    email: Optional[str] = None