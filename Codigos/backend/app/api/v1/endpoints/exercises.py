"""
@file exercises.py
@brief Define os endpoints da API para análise de exercícios em tempo real e consulta de instruções.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any

from app.models.user import User
from app.core.dependencies import get_current_active_user
# O nome do serviço foi inferido a partir do uso no código.
from app.services import pose_estimation_service

# Cria uma nova instância de roteador para os endpoints de análise de exercícios.
router = APIRouter()

class ExerciseRequest(BaseModel):
    """Schema para a requisição de análise de exercício.

    Attributes:
        exercise_type (str): O tipo de exercício a ser analisado (ex: "squat").
        image_b64 (str): O frame do vídeo codificado como uma string base64.
    """
    exercise_type: str
    image_b64: str

@router.get("/{exercise_id}/instructions", response_model=Dict[str, str])
def get_exercise_instructions(
    exercise_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Retorna as instruções de execução para um exercício específico.

    Este endpoint contém instruções pré-definidas para um conjunto fixo de exercícios.
    Requer um utilizador autenticado e ativo.

    :param (str) exercise_id: O identificador do exercício (ex: "squat", "push_up").
    :param (User) current_user: O utilizador autenticado.
    :raises HTTPException: Se o 'exercise_id' não corresponder a nenhum exercício conhecido.
    :return (Dict[str, str]): Um dicionário contendo as instruções formatadas.
    """
    # Nota: As instruções estão pré-definidas no código.
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
    """Recebe um frame de vídeo e o tipo de exercício para análise.

    Delega a análise para o serviço de estimativa de pose, que retorna a
    contagem de repetições, estágio do movimento e feedback de postura.

    :param (ExerciseRequest) request: O corpo da requisição com o tipo de exercício e a imagem em base64.
    :param (User) current_user: O utilizador autenticado.
    :raises HTTPException: Se a requisição for inválida ou se ocorrer um erro interno.
    :return (Dict[str, Any]): Um dicionário com os resultados da análise.
    """
    try:
        analysis_result = pose_estimation_service.analyze_exercise_frame(
            exercise_type=request.exercise_type,
            image_b64=request.image_b64
        )
        return analysis_result
    except ValueError as e:
        # Erros de validação, como tipo de exercício não suportado ou imagem inválida.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        # Captura outras exceções inesperadas durante a análise.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro interno durante a análise: {e}",
        )
