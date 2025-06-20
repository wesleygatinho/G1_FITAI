from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Any, List
from sqlalchemy.orm import Session
import uuid

# Importações dos módulos da aplicação
from app.models.user import User as UserModel
from app.core.dependencies import get_current_active_user
# Esta importação agora funcionará porque o nome do ficheiro foi corrigido
from app.services import ai_generation_service
from app.services import crud
from app.core.database import get_db
from app.schemas.ia_interaction import RegistroInteracaoIA, RegistroInteracaoIACreate

router = APIRouter()

# --- Schemas para as requisições e respostas da API ---

class PlanRequest(BaseModel):
    prompt: str

class TipResponse(BaseModel):
    tip: str

class PlanResponse(BaseModel):
    plan: str

# --- Endpoints ---

@router.get("/tips/daily", response_model=TipResponse, status_code=status.HTTP_200_OK)
def get_daily_tip(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user)
):
    interaction_result = ai_generation_service.get_daily_fitness_tip()
    if "error" in interaction_result:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=interaction_result["error"])
    
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
    interactions = crud.get_ia_interactions_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return interactions
