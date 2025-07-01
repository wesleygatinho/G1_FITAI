"""
@file main.py
@brief Arquivo principal para inicialização da API FitAI, configuração dos endpoints e população inicial da base de dados.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""
import sys
import os
from sqlalchemy.orm import Session

# Adiciona o diretório raiz do projeto ao caminho de pesquisa do Python para permitir importações absolutas.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, SessionLocal
from app.api.v1.api import api_router
# Importar todos os modelos para que o SQLAlchemy possa criar as tabelas.
from app.models import user, progress_record, exercise_session, exercicio
from app.services import crud
from app.schemas.exercicio import ExercicioCreate

# Cria todas as tabelas na base de dados, caso ainda não existam.
user.Base.metadata.create_all(bind=engine)


def populate_initial_exercises():
    """Popula a base de dados com um conjunto inicial de exercícios.

    Esta função verifica se os exercícios padrão ('squat', 'push_up', 'hammer_curl')
    já existem na base de dados. Caso não existam, eles são criados e adicionados.
    A conexão com a base de dados é aberta no início da função e fechada ao final.

    :return: None
    """
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
        # Verifica se o exercício já existe antes de o criar para evitar duplicatas.
        db_exercicio = crud.get_exercicio_by_nome(db, nome=ex.nome)
        if not db_exercicio:
            print(f"A criar exercício inicial: {ex.nome}")
            crud.create_exercicio(db, exercicio=ex)
            
    db.close()

# Popula a base de dados com os exercícios iniciais na inicialização da aplicação.
populate_initial_exercises()

# Instancia a aplicação FastAPI com metadados para a documentação.
app = FastAPI(
    title="FitAI API",
    description="A API para o aplicativo de monitoramento de exercícios FitAI.",
    version="1.0.0"
)

# Configura o CORS para permitir requisições de qualquer origem,
# o que é útil para ambientes de desenvolvimento com front-ends separados.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui o roteador da API v1, prefixando todas as rotas com /api/v1.
app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint principal (raiz) da API.

    Retorna uma mensagem de boas-vindas simples para verificar se a API está
    operacional.

    :return (dict): Uma mensagem de boas-vindas em formato JSON.
    """
    return {"message": "Bem-vindo à API do FitAI!"}
