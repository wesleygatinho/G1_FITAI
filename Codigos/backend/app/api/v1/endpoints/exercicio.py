"""
@file exercicio.py
@brief Define os endpoints da API para a gestão e consulta de exercícios.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict

# Importações dos módulos da aplicação
from app.schemas import exercicio as exercicio_schema
from app.core.database import get_db
from app.services import crud
from app.core.dependencies import get_current_active_user
from app.models.user import User as UserModel

# Cria uma nova instância de roteador para os endpoints de gestão de exercícios.
router = APIRouter()

@router.get("/", response_model=List[exercicio_schema.Exercicio])
def read_exercicios(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_active_user)
):
    """Recupera uma lista paginada de todos os exercícios disponíveis.

    Este endpoint requer um utilizador autenticado e ativo.

    :param (Session) db: A sessão da base de dados.
    :param (int) skip: O número de exercícios a pular (para paginação).
    :param (int) limit: O número máximo de exercícios a retornar.
    :param (UserModel) current_user: O utilizador autenticado.
    :return (List[exercicio_schema.Exercicio]): Uma lista de objetos de exercício.
    """
    exercicios = crud.get_exercicios(db, skip=skip, limit=limit)
    return exercicios

@router.get("/{exercise_name}/instructions", response_model=Dict[str, str])
def get_exercise_instructions(
    exercise_name: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Retorna as instruções de execução para um exercício específico, procurando-o pelo nome.

    :param (str) exercise_name: O nome do exercício (ex: "squat") passado no URL.
    :param (Session) db: A sessão da base de dados.
    :param (UserModel) current_user: O utilizador autenticado.
    :raises HTTPException: Se o exercício ou as suas instruções não forem encontrados.
    :return (Dict[str, str]): Um dicionário contendo as instruções do exercício.
    """
    db_exercicio = crud.get_exercicio_by_nome(db, nome=exercise_name)

    if not db_exercicio or not db_exercicio.instrucoes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Instruções não encontradas para este exercício."
        )
    
    return {"instructions": db_exercicio.instrucoes}
