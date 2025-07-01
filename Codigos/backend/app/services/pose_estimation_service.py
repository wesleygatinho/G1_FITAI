"""
@file pose_estimation_service.py
@brief Orquestra a análise de frames de exercícios, da decodificação à contagem.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""

import cv2
import numpy as np
import base64

from exercises.estimation import PoseEstimator
from exercises.squat import Squat
from exercises.push_up import PushUp
from exercises.hummer_curl import HammerCurl

# Instância global do estimador de pose, para não ser recriado a cada chamada.
pose_estimator = PoseEstimator()
# Dicionário que mapeia os tipos de exercício para suas classes de rastreamento.
exercise_trackers = {"squat": Squat(), "push_up": PushUp(), "hammer_curl": HammerCurl()}

def analyze_exercise_frame(exercise_type: str, image_b64: str):
    """Analisa um único frame de um exercício recebido como uma string base64.

    Esta função decodifica a imagem, executa a estimativa de pose para encontrar
    os marcos corporais e, em seguida, passa esses marcos para o rastreador de
    exercício específico para análise de movimento, contagem e feedback.

    :param (str) exercise_type: O tipo de exercício a ser analisado ('squat', 'push_up', 'hammer_curl').
    :param (str) image_b64: A imagem do frame codificada em formato base64.
    :raises ValueError: Se o tipo de exercício não for suportado ou se a imagem for inválida.
    :return (dict): Um dicionário contendo os dados da análise ou uma mensagem de erro.
    """
    if exercise_type not in exercise_trackers:
        raise ValueError("Exercício não suportado")

    try:
        # Decodifica a imagem de base64 para um formato que o OpenCV entende.
        img_bytes = base64.b64decode(image_b64)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None: raise ValueError("Não foi possível decodificar a imagem.")
    except Exception:
        raise ValueError("String base64 da imagem inválida ou corrompida.")

    # Usa o estimador de pose para encontrar os marcos corporais no frame.
    results = pose_estimator.estimate_pose(frame)
    if not results.pose_landmarks:
        return {"error": "Nenhum corpo detetado na imagem."}

    # Seleciona o rastreador correto com base no tipo de exercício.
    tracker = exercise_trackers[exercise_type]
    
    # --- LÓGICA GENERALIZADA ---
    # Chama o método de rastreamento apropriado. Todos os trackers devem
    # retornar uma tupla com 6 valores para manter a consistência.
    if exercise_type == "squat":
        counter, angle, stage, feedback, landmarks, progress = tracker.track_squat(results.pose_landmarks.landmark, frame.shape)
    elif exercise_type == "push_up":
        counter, angle, stage, feedback, landmarks, progress = tracker.track_push_up(results.pose_landmarks.landmark, frame.shape)
    elif exercise_type == "hammer_curl":
        counter, angle, stage, feedback, landmarks, progress = tracker.track_hammer_curl(results.pose_landmarks.landmark, frame.shape)
    else:
        # Este caso é redundante devido à verificação inicial, mas é uma boa prática.
        return {"error": "Lógica de análise não implementada."}
    
    # Retorna uma resposta JSON consistente para a interface do utilizador.
    return {
        "counter": counter, 
        "stage": stage, 
        "feedback": feedback,
        "landmarks": landmarks,
        "progress": progress
    }