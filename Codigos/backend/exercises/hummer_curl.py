import numpy as np
from .angle_calculation import calculate_angle

class HammerCurl:
    def __init__(self):
        self.counter = 0
        self.stage = "down"
        self.feedback = "Inicie o movimento"
        # Definir os ângulos mínimo e máximo do movimento
        self.angle_min = 30
        self.angle_max = 160

    def track_hammer_curl(self, landmarks, frame_shape):
        # Extrai os pontos relevantes para ambos os braços
        shoulder_left = [landmarks[12].x, landmarks[12].y]
        elbow_left = [landmarks[14].x, landmarks[14].y]
        wrist_left = [landmarks[16].x, landmarks[16].y]
        shoulder_right = [landmarks[11].x, landmarks[11].y]
        elbow_right = [landmarks[13].x, landmarks[13].y]
        wrist_right = [landmarks[15].x, landmarks[15].y]
        
        # Usa o ângulo do braço direito como referência principal
        angle = calculate_angle((shoulder_right[0], shoulder_right[1]), (elbow_right[0], elbow_right[1]), (wrist_right[0], wrist_right[1]))
        
        # --- LÓGICA DE PROGRESSO E CONTAGEM ---
        progress = np.interp(angle, [self.angle_min, self.angle_max], [100, 0])

        if angle > self.angle_max: # Braço esticado
            self.stage = "down"
        elif angle < self.angle_min and self.stage == 'down': # Braço contraído
            self.stage = "up"
            self.counter += 1
            self.feedback = "Desça de forma controlada"
            
        landmarks_to_draw = {
            "shoulder_left": shoulder_left,
            "elbow_left": elbow_left,
            "wrist_left": wrist_left,
            "shoulder_right": shoulder_right,
            "elbow_right": elbow_right,
            "wrist_right": wrist_right,
        }
        
        return self.counter, angle, self.stage, self.feedback, landmarks_to_draw, progress
