from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict

# Importar os módulos necessários
from app.schemas import exercicio as exercicio_schema
from app.core.database import get_db
from app.services import crud
from app.core.dependencies import get_current_active_user
from app.models.user import User as UserModel

router = APIRouter()

@router.get("/", response_model=List[exercicio_schema.Exercicio])
def read_exercicios(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_active_user)
):
    """
    Recupera uma lista de todos os exercícios disponíveis na base de dados.
    """
    exercicios = crud.get_exercicios(db, skip=skip, limit=limit)
    return exercicios

# --- ENDPOINT CORRIGIDO ---
@router.get("/{exercise_name}/instructions", response_model=Dict[str, str])
def get_exercise_instructions(
    exercise_name: str, # Agora aceita o nome do exercício
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """
    Retorna as instruções de execução para um exercício específico, procurando-o pelo nome.
    """
    # Procura o exercício na base de dados pelo nome que vem do URL
    db_exercicio = crud.get_exercicio_by_nome(db, nome=exercise_name)

    if not db_exercicio or not db_exercicio.instrucoes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Instruções não encontradas para este exercício."
        )
    
    # Retorna as instruções encontradas na base de dados
    return {"instructions": db_exercicio.instrucoes}
