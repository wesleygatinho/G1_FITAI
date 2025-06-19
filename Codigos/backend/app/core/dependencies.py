from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.services import crud
from app.schemas.token import TokenData
from app.models.user import User
from app.core.config import settings
from app.core.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
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
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Utilizador inativo")
    return current_user



# from fastapi import Depends, HTTPException
# from sqlalchemy.orm import Session

# from app.services import crud
# from app.models.user import User
# from app.core.database import get_db

# def get_current_active_user(db: Session = Depends(get_db)) -> User:
#     """
#     MODO DE TESTE: Esta função não valida um token.
#     Em vez disso, retorna um utilizador de teste pré-definido.
#     """
#     user = crud.get_user_by_email(db, email="test@fitai.com")
#     if not user:
#         raise HTTPException(
#             status_code=404, 
#             detail="Utilizador de teste 'test@fitai.com' não encontrado. Reinicie o servidor."
#         )
#     if not user.is_active:
#         raise HTTPException(status_code=400, detail="Utilizador inativo")
    
#     # Retorna sempre o mesmo utilizador para todos os endpoints protegidos
#     return user