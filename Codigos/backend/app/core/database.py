from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

# Cria o "motor" do SQLAlchemy que se conectará ao banco de dados
# O 'pool_pre_ping=True' verifica as conexões antes de usá-las,
# o que pode prevenir erros com conexões que foram fechadas pelo DB.
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

# Cria uma classe SessionLocal, que será a fábrica para novas sessões de banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para obter uma sessão de banco de dados.
# Isso será usado como uma dependência em nossos endpoints da API.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()