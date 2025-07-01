"""
@file database.py
@brief Configura a conexão com a base de dados e a gestão de sessões do SQLAlchemy.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

# Cria o "motor" (engine) do SQLAlchemy que se conectará à base de dados.
# A URL é lida a partir das configurações da aplicação.
# O argumento 'pool_pre_ping=True' verifica as conexões antes de usá-las,
# o que previne erros com conexões que foram fechadas pelo servidor da base de dados.
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

# Cria uma classe SessionLocal, que funcionará como uma fábrica para novas sessões de base de dados.
# autocommit=False e autoflush=False são as configurações padrão e mais seguras para
# controlar as transações manualmente.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Fornece uma sessão de base de dados para ser usada como dependência nos endpoints.

    Esta função geradora cria uma nova sessão para cada requisição, disponibiliza-a
    e garante que seja sempre fechada no final, mesmo que ocorram erros.

    :return (Generator): Um gerador que fornece uma instância da sessão do SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
