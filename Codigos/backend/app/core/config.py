import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Classe para gerenciar as configurações da aplicação.
    """
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://andre:12345@localhost:5432/fitai_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "uma-chave-secreta-muito-longa-e-aleatoria")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- CHAVE DA API ATUALIZADA PARA O GOOGLE GEMINI ---
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "CHAVE_NAO_CONFIGURADA")

    class Config:
        case_sensitive = True

settings = Settings()
