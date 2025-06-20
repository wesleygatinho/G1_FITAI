import cv2
import numpy as np
import base64

from exercises.estimation import PoseEstimator
from exercises.squat import Squat
from exercises.push_up import PushUp
from exercises.hummer_curl import HammerCurl

pose_estimator = PoseEstimator()
exercise_trackers = {"squat": Squat(), "push_up": PushUp(), "hammer_curl": HammerCurl()}

def analyze_exercise_frame(exercise_type: str, image_b64: str):
    if exercise_type not in exercise_trackers:
        raise ValueError("Exercício não suportado")

    try:
        img_bytes = base64.b64decode(image_b64)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None: raise ValueError("Não foi possível decodificar a imagem.")
    except Exception:
        raise ValueError("String base64 da imagem inválida ou corrompida.")

    results = pose_estimator.estimate_pose(frame)
    if not results.pose_landmarks:
        return {"error": "Nenhum corpo detetado na imagem."}

    tracker = exercise_trackers[exercise_type]
    
    # --- LÓGICA GENERALIZADA ---
    # Todos os trackers agora retornam 6 valores
    if exercise_type == "squat":
        counter, angle, stage, feedback, landmarks, progress = tracker.track_squat(results.pose_landmarks.landmark, frame.shape)
    elif exercise_type == "push_up":
        counter, angle, stage, feedback, landmarks, progress = tracker.track_push_up(results.pose_landmarks.landmark, frame.shape)
    elif exercise_type == "hammer_curl":
        counter, angle, stage, feedback, landmarks, progress = tracker.track_hammer_curl(results.pose_landmarks.landmark, frame.shape)
    else:
        return {"error": "Lógica de análise não implementada."}
    
    # Retorna uma resposta JSON consistente
    return {
        "counter": counter, 
        "stage": stage, 
        "feedback": feedback,
        "landmarks": landmarks,
        "progress": progress
    }
