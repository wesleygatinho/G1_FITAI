import numpy as np
from .angle_calculation import calculate_angle

class PushUp:
    def __init__(self):
        self.counter = 0
        self.stage = "up"
        self.feedback = "Posição inicial"
        # Definir os ângulos mínimo e máximo do movimento
        self.angle_min = 70
        self.angle_max = 160

    def track_push_up(self, landmarks, frame_shape):
        # Extrai os pontos relevantes para ambos os braços (coordenadas normalizadas)
        shoulder_left = [landmarks[11].x, landmarks[11].y]
        elbow_left = [landmarks[13].x, landmarks[13].y]
        wrist_left = [landmarks[15].x, landmarks[15].y]
        shoulder_right = [landmarks[12].x, landmarks[12].y]
        elbow_right = [landmarks[14].x, landmarks[14].y]
        wrist_right = [landmarks[16].x, landmarks[16].y]
        
        # Usa o ângulo do braço esquerdo para a análise (pode ser a média se preferir)
        angle = calculate_angle((shoulder_left[0], shoulder_left[1]), (elbow_left[0], elbow_left[1]), (wrist_left[0], wrist_left[1]))
        
        # --- LÓGICA DE PROGRESSO E CONTAGEM ---
        progress = np.interp(angle, [self.angle_min, self.angle_max], [100, 0])

        if angle > self.angle_max:
            if self.stage == 'down':
                self.feedback = "Excelente! Prepare para a próxima."
            self.stage = "up"
        elif angle < self.angle_min and self.stage == 'up':
            self.stage = "down"
            self.counter += 1
            self.feedback = "Suba com força!"
        
        # Estrutura de retorno de dados para o frontend
        landmarks_to_draw = {
            "shoulder_left": shoulder_left,
            "elbow_left": elbow_left,
            "wrist_left": wrist_left,
            "shoulder_right": shoulder_right,
            "elbow_right": elbow_right,
            "wrist_right": wrist_right,
        }
        
        return self.counter, angle, self.stage, self.feedback, landmarks_to_draw, progress
