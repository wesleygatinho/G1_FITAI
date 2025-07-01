"""
@file config.py
@brief Centraliza as configurações da aplicação, carregadas a partir de variáveis de ambiente.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Carrega as variáveis de ambiente de um ficheiro .env para o ambiente do sistema.
load_dotenv()

class Settings(BaseSettings):
    """Classe para gerenciar as configurações da aplicação.

    Lê as configurações a partir de variáveis de ambiente, com valores padrão
    de fallback para um ambiente de desenvolvimento local.

    Attributes:
        DATABASE_URL (str): URL de conexão com a base de dados PostgreSQL.
        SECRET_KEY (str): Chave secreta usada para assinar os tokens JWT.
        ALGORITHM (str): Algoritmo de criptografia para os tokens JWT.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Tempo de expiração do token de acesso em minutos.
        GOOGLE_API_KEY (str): Chave da API para aceder aos serviços do Google Gemini.
        GOOGLE_CLIENT_ID (str): Credencial para o login social com o Google (OAuth2).
        GOOGLE_CLIENT_SECRET (str): Credencial para o login social com o Google (OAuth2).
    """
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/fitai_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "uma-chave-secreta-muito-longa-e-aleatoria")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "CHAVE_NAO_CONFIGURADA")

    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")


    class Config:
        """Configuração do Pydantic Settings."""
        # Garante que os nomes das variáveis de ambiente correspondam exatamente.
        case_sensitive = True

# Instância única das configurações para ser importada e utilizada em toda a aplicação.
settings = Settings()
