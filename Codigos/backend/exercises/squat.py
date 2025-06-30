import numpy as np

class Squat:
    def __init__(self):
        self.stage = "up"
        self.counter = 0
        self.feedback = ""

    def calculate_angle(self, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle

    def track_squat(self, landmarks, image_shape):
        self.feedback = "" # Limpa o feedback a cada frame

        # --- CORREÇÃO APLICADA AQUI ---
        # Adiciona um bloco try-except para garantir que todos os landmarks existem
        try:
            # Pega as coordenadas dos pontos de referência necessários
            hip = [landmarks[23].x, landmarks[23].y]
            knee = [landmarks[25].x, landmarks[25].y]
            ankle = [landmarks[27].x, landmarks[27].y]
            shoulder = [landmarks[11].x, landmarks[11].y]

        except (IndexError, AttributeError):
            # Se um ponto não for encontrado, retorna o feedback de erro
            self.feedback = "Enquadramento ruim! Posicione a câmera para que seu corpo inteiro (dos ombros aos pés) apareça."
            return self.counter, 0, self.stage, self.feedback, {}, 0

        # Lógica de cálculo de ângulo e contagem (original, mas agora segura)
        angle = self.calculate_angle(hip, knee, ankle)
        progress = np.interp(angle, [90, 160], [100, 0])

        if angle > 160:
            self.stage = "up"
        if angle < 90 and self.stage == 'up':
            self.stage = "down"
            self.counter += 1
            self.feedback = "Repetição completa!"
        
        # Feedback de profundidade
        if self.stage == 'down' and angle > 100:
            self.feedback = "Desça mais para um agachamento completo."
        
        # Feedback de postura (tronco)
        angle_trunk = self.calculate_angle(shoulder, hip, knee)
        if angle_trunk < 70:
            self.feedback = "Mantenha o peito aberto e as costas retas."

        if not self.feedback:
            self.feedback = "Bom trabalho, continue!"

        # Converte landmarks para o formato de dicionário para o JSON
        landmarks_dict = {str(i): {'x': lm.x, 'y': lm.y, 'z': lm.z, 'visibility': lm.visibility} for i, lm in enumerate(landmarks)}

        return self.counter, angle, self.stage, self.feedback, landmarks_dict, progress