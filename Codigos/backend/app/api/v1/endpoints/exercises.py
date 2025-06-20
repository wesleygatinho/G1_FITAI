from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any

from app.models.user import User
from app.core.dependencies import get_current_active_user
from app.services import pose_estimation_service

router = APIRouter()

class ExerciseRequest(BaseModel):
    """Schema para a requisição de análise de exercício."""
    exercise_type: str
    image_b64: str

# --- NOVO ENDPOINT DE INSTRUÇÕES ---
@router.get("/{exercise_id}/instructions", response_model=Dict[str, str])
def get_exercise_instructions(
    exercise_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Retorna as instruções de execução para um exercício específico.
    """
    instructions = {
        "squat": """
### Posição Inicial:
1. Fique de pé com os pés afastados na largura dos ombros.
2. Mantenha as costas retas e o peito aberto.

### Execução:
1. Agache como se fosse sentar numa cadeira, empurrando os quadris para trás.
2. Desça até que as suas coxas fiquem paralelas ao chão.
3. Suba de volta à posição inicial, impulsionando com os calcanhares.
        """,
        "push_up": """
### Posição Inicial:
1. Fique em posição de prancha, com as mãos diretamente abaixo dos ombros.
2. Mantenha o corpo reto da cabeça aos calcanhares.

### Execução:
1. Baixe o corpo até que o peito quase toque no chão.
2. Empurre o corpo para cima até à posição inicial.
        """,
        "hammer_curl": """
### Posição Inicial:
1. Segure um haltere em cada mão com as palmas viradas uma para a outra.
2. Mantenha os cotovelos junto ao corpo.

### Execução:
1. Levante os halteres em direção aos ombros, mantendo as palmas viradas para dentro.
2. Baixe os halteres de forma controlada até à posição inicial.
        """
    }

    if exercise_id not in instructions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercício não encontrado")
    
    return {"instructions": instructions[exercise_id]}


@router.post("/analyze", response_model=Dict[str, Any])
def analyze_exercise(
    request: ExerciseRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Recebe um frame de vídeo (como imagem base64) e o tipo de exercício,
    e retorna a análise de contagem de repetições e feedback de postura.
    """
    try:
        analysis_result = pose_estimation_service.analyze_exercise_frame(
            exercise_type=request.exercise_type,
            image_b64=request.image_b64
        )
        return analysis_result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro interno durante a análise: {e}",
        )
