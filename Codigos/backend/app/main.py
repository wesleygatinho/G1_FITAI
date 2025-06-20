import sys
import os
from sqlalchemy.orm import Session

# Adiciona o diretório 'backend' ao caminho de pesquisa do Python.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, SessionLocal
from app.api.v1.api import api_router
# Importar todos os modelos para que o SQLAlchemy os possa criar
from app.models import user, progress_record, exercise_session, exercicio
from app.services import crud
from app.schemas.exercicio import ExercicioCreate

# Cria todas as tabelas na base de dados.
user.Base.metadata.create_all(bind=engine)


# --- NOVA FUNÇÃO PARA POPULAR A BASE DE DADOS COM EXERCÍCIOS ---
def populate_initial_exercises():
    db: Session = SessionLocal()
    
    initial_exercises = [
        ExercicioCreate(
            nome="squat", 
            descricao="Um exercício fundamental para fortalecer pernas e glúteos.", 
            instrucoes="Mantenha as costas retas e agache até as coxas ficarem paralelas ao chão."
        ),
        ExercicioCreate(
            nome="push_up", 
            descricao="Excelente para peito, ombros e tríceps.", 
            instrucoes="Mantenha o corpo reto e desça até o peito quase tocar no chão."
        ),
        ExercicioCreate(
            nome="hammer_curl", 
            descricao="Focado no fortalecimento dos bíceps e antebraços.", 
            instrucoes="Levante os pesos com as palmas das mãos viradas uma para a outra."
        ),
    ]

    for ex in initial_exercises:
        # Verifica se o exercício já existe antes de o criar
        db_exercicio = crud.get_exercicio_by_nome(db, nome=ex.nome)
        if not db_exercicio:
            print(f"A criar exercício inicial: {ex.nome}")
            crud.create_exercicio(db, exercicio=ex)
            
    db.close()
# --------------------------------------------------------------------

# Popula a base de dados ao iniciar
populate_initial_exercises()


app = FastAPI(
    title="FitAI API",
    description="A API para o aplicativo de monitoramento de exercícios FitAI.",
    version="1.0.0"
)

# ... (resto do ficheiro main.py, incluindo CORS e routers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API do FitAI!"}
