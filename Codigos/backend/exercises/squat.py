"""
@file squat.py
@brief Contém a lógica de rastreamento e contagem para o exercício de agachamento (Squat).
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""
import numpy as np
from .angle_calculation import calculate_angle

class Squat:
    """Gerencia o estado, contagem de repetições e feedback para o exercício de agachamento.

    Esta classe utiliza os marcos de pose para calcular os ângulos do joelho e do tronco,
    contar as repetições e fornecer feedback sobre a profundidade e a postura.

    Attributes:
        stage (str): O estágio atual do exercício, podendo ser 'up' (em pé) ou 'down' (agachado).
        counter (int): Contador de repetições completas.
        feedback (str): Mensagem de texto para orientar o usuário.
        angle_min (int): Ângulo mínimo do joelho para registrar a fase 'down'.
        angle_max (int): Ângulo máximo do joelho para registrar a fase 'up'.
    """
    def __init__(self):
        """Inicializa o rastreador do exercício de agachamento.

        Define os valores iniciais para o contador, o estágio do movimento e os
        limites de ângulo que caracterizam a repetição.
        """
        self.stage = "up"
        self.counter = 0
        self.feedback = ""
        self.angle_min = 90
        self.angle_max = 160

    def track_squat(self, landmarks, image_shape):
        """Processa os marcos de pose para rastrear uma repetição do agachamento.

        Verifica a visibilidade dos marcos, calcula ângulos, atualiza o estágio do
        movimento, incrementa o contador e gera feedback de profundidade e postura.

        :param (object) landmarks: O objeto de resultados do MediaPipe com a lista de marcos da pose.
        :param (tuple) image_shape: A forma (altura, largura) do quadro (não utilizado).
        :return (tuple): Uma tupla contendo (contador, ângulo, estágio, feedback, marcos, progresso).
        """
        self.feedback = "" # Limpa o feedback a cada frame

        try:
            # Extrai as coordenadas dos pontos de referência necessários
            hip = [landmarks[23].x, landmarks[23].y]
            knee = [landmarks[25].x, landmarks[25].y]
            ankle = [landmarks[27].x, landmarks[27].y]
            shoulder = [landmarks[11].x, landmarks[11].y]

        except (IndexError, AttributeError):
            # Se um ponto não for encontrado, retorna feedback de erro.
            self.feedback = "Enquadramento ruim! Posicione a câmera para que seu corpo inteiro (dos ombros aos pés) apareça."
            return self.counter, 0, self.stage, self.feedback, {}, 0

        # Calcula o ângulo do joelho para a lógica de contagem.
        angle = calculate_angle(hip, knee, ankle)
        progress = np.interp(angle, [self.angle_min, self.angle_max], [100, 0])

        # Lógica de contagem baseada no ângulo do joelho.
        if angle > self.angle_max:
            self.stage = "up"
        if angle < self.angle_min and self.stage == 'up':
            self.stage = "down"
            self.counter += 1
            self.feedback = "Repetição completa!"
        
        # Feedback sobre a profundidade do agachamento.
        if self.stage == 'down' and angle > 100:
            self.feedback = "Desça mais para um agachamento completo."
        
        # Feedback sobre a postura do tronco.
        angle_trunk = calculate_angle(shoulder, hip, knee)
        if angle_trunk < 70:
            self.feedback = "Mantenha o peito aberto e as costas retas."

        if not self.feedback and self.stage == 'up':
            self.feedback = "Inicie o movimento"
        elif not self.feedback and self.stage == 'down':
             self.feedback = "Suba com força!"


        # Agrupa os marcos relevantes para facilitar o desenho na interface
        landmarks_to_draw = {
            "hip": hip,
            "knee": knee,
            "ankle": ankle,
            "shoulder": shoulder,
        }

        return self.counter, angle, self.stage, self.feedback, landmarks_to_draw, progress
