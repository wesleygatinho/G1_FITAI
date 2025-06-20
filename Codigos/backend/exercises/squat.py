import cv2
# O ficheiro angle_calculation.py não precisa de alterações
from .angle_calculation import calculate_angle

class Squat:
    def __init__(self):
        self.counter = 0
        self.stage = "up"
        self.feedback = "Inicie o movimento"

    def _calculate_angle(self, p1, p2, p3):
        # Esta função está definida em angle_calculation.py
        return calculate_angle(p1, p2, p3)

    def track_squat(self, landmarks, frame_shape):
        # Extrai os pontos relevantes do corpo (coordenadas normalizadas de 0.0 a 1.0)
        shoulder = [landmarks[11].x, landmarks[11].y]
        hip = [landmarks[23].x, landmarks[23].y]
        knee = [landmarks[25].x, landmarks[25].y]
        ankle = [landmarks[27].x, landmarks[27].y]

        # Calcula o ângulo do joelho
        angle = self._calculate_angle(
            (hip[0], hip[1]), 
            (knee[0], knee[1]), 
            (ankle[0], ankle[1])
        )

        # Lógica de contagem de repetições e feedback
        if angle > 160: # Se o utilizador está de pé
            if self.stage == 'down':
                # Só dá feedback de "bom trabalho" se a fase anterior foi "para baixo"
                self.feedback = "Bom trabalho! Inicie a próxima repetição."
            self.stage = "up"
        elif angle < 90 and self.stage == 'up': # Se o utilizador agachou
            self.stage = "down"
            self.counter += 1
            self.feedback = "Suba de forma controlada!"
        elif self.stage == 'up' and angle < 160 and angle >= 90:
            self.feedback = "Desça mais um pouco!"
        
        # Estrutura de retorno de dados melhorada para o frontend
        landmarks_to_draw = {
            "shoulder": shoulder,
            "hip": hip,
            "knee": knee,
            "ankle": ankle,
        }

        # Retorna todos os dados para a API
        return self.counter, angle, self.stage, self.feedback, landmarks_to_draw
