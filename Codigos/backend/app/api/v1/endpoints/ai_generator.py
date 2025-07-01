"""
@file ai_generator.py
@brief Define os endpoints da API para interações com o serviço de IA generativa.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Any, List
from sqlalchemy.orm import Session
import uuid

# Importações dos módulos da aplicação
from app.models.user import User as UserModel
from app.core.dependencies import get_current_active_user
from app.services.ai_generation_service import ai_generation_service
from app.services import crud
from app.core.database import get_db
from app.schemas.ia_interaction import RegistroInteracaoIA, RegistroInteracaoIACreate

# Cria uma nova instância de roteador para os endpoints de IA.
router = APIRouter()

class PlanRequest(BaseModel):
    """Schema para a requisição de geração de plano de treino.

    Attributes:
        prompt (str): O prompt do utilizador para a IA.
    """
    prompt: str

class TipResponse(BaseModel):
    """Schema para a resposta da dica diária.

    Attributes:
        tip (str): A dica de fitness gerada pela IA.
    """
    tip: str

class PlanResponse(BaseModel):
    """Schema para a resposta do plano de treino gerado.

    Attributes:
        plan (str): O plano de treino gerado pela IA.
    """
    plan: str


@router.get("/tips/daily", response_model=TipResponse, status_code=status.HTTP_200_OK)
def get_daily_tip(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Fornece uma dica de fitness diária gerada pela IA.

    Este endpoint requer um utilizador autenticado e ativo. Ele chama o serviço de IA,
    salva a interação na base de dados e retorna a dica.

    :param (Session) db: A sessão da base de dados.
    :param (UserModel) current_user: O utilizador autenticado.
    :raises HTTPException: Se o serviço de IA não estiver disponível.
    :return (TipResponse): Um objeto JSON com a dica do dia.
    """
    interaction_result = ai_generation_service.get_daily_fitness_tip()
    if "error" in interaction_result:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=interaction_result["error"])
    
    # Salva a interação na base de dados para o histórico do utilizador.
    interaction_to_save = RegistroInteracaoIACreate(
        prompt_usuario=interaction_result["prompt_usuario"],
        resposta_ia=interaction_result["resposta_ia"]
    )
    crud.create_ia_interaction(db=db, interaction=interaction_to_save, user_id=current_user.id)

    return {"tip": interaction_result["resposta_ia"]}

@router.post("/plans/generate", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
def generate_plan(
    request: PlanRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    """Gera um plano de treino personalizado com base no prompt do utilizador.

    Valida o prompt, chama o serviço de IA para gerar o plano, salva a interação
    e retorna o plano de treino.

    :param (PlanRequest) request: O corpo da requisição com o prompt do utilizador.
    :param (Session) db: A sessão da base de dados.
    :param (UserModel) current_user: O utilizador autenticado.
    :raises HTTPException: Se o prompt for muito curto ou se o serviço de IA falhar.
    :return (PlanResponse): Um objeto JSON com o plano de treino gerado.
    """
    if not request.prompt or len(request.prompt) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O prompt deve ter pelo menos 10 caracteres."
        )
    
    interaction_result = ai_generation_service.generate_custom_workout_plan(prompt=request.prompt)
    if "error" in interaction_result:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=interaction_result["error"])

    interaction_to_save = RegistroInteracaoIACreate(
        prompt_usuario=interaction_result["prompt_usuario"],
        resposta_ia=interaction_result["resposta_ia"]
    )
    crud.create_ia_interaction(db=db, interaction=interaction_to_save, user_id=current_user.id)
    
    return {"plan": interaction_result["resposta_ia"]}

@router.get("/interactions/history", response_model=List[RegistroInteracaoIA], status_code=status.HTTP_200_OK)
def read_ia_interaction_history(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_active_user)
):
    """Obtém o histórico de interações do utilizador com a IA.

    Retorna uma lista paginada de todas as interações passadas entre o
    utilizador autenticado e o serviço de IA.

    :param (Session) db: A sessão da base de dados.
    :param (int) skip: O número de registos a pular (para paginação).
    :param (int) limit: O número máximo de registos a retornar.
    :param (UserModel) current_user: O utilizador autenticado.
    :return (List[RegistroInteracaoIA]): Uma lista de registos de interação.
    """
    interactions = crud.get_ia_interactions_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return interactions
