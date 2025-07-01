"""
@file push_up.py
@brief Contém a lógica de rastreamento e contagem para o exercício de flexão (Push-Up).
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""
import numpy as np
from .angle_calculation import calculate_angle

class PushUp:
    """Gerencia o estado, a contagem e o feedback para o exercício de flexão.

    Esta classe utiliza os marcos de pose para calcular o ângulo do cotovelo,
    contar as repetições e fornecer feedback sobre a execução do movimento de flexão.

    Attributes:
        counter (int): Contador de repetições completas.
        stage (str): Estágio atual do exercício, 'up' (subida) ou 'down' (descida).
        feedback (str): Mensagem de texto para orientar o usuário.
        angle_min (int): Ângulo mínimo do cotovelo para registrar a fase 'down'.
        angle_max (int): Ângulo máximo do cotovelo para registrar a fase 'up'.
    """
    def __init__(self):
        """Inicializa o rastreador do exercício de flexão.

        Define os valores iniciais para o contador, o estágio do movimento (começando
        em 'up') e os limites de ângulo que caracterizam a repetição.
        """
        self.counter = 0
        self.stage = "up"
        self.feedback = "Posição inicial"
        # Define os ângulos mínimo e máximo do movimento
        self.angle_min = 70
        self.angle_max = 160

    def track_push_up(self, landmarks, frame_shape):
        """Processa os marcos de pose para rastrear uma repetição do exercício de flexão.

        Calcula o ângulo do cotovelo esquerdo, atualiza o estágio do movimento,
        incrementa o contador e gera feedback para o usuário.

        :param (object) landmarks: O objeto de resultados do MediaPipe com os marcos da pose.
        :param (tuple) frame_shape: A forma (altura, largura) do quadro (não utilizado diretamente).
        :return (tuple): Uma tupla contendo (contador, ângulo, estágio, feedback, marcos, progresso).
        """
        # Extrai as coordenadas dos pontos relevantes para os braços
        shoulder_left = [landmarks[11].x, landmarks[11].y]
        elbow_left = [landmarks[13].x, landmarks[13].y]
        wrist_left = [landmarks[15].x, landmarks[15].y]
        shoulder_right = [landmarks[12].x, landmarks[12].y]
        elbow_right = [landmarks[14].x, landmarks[14].y]
        wrist_right = [landmarks[16].x, landmarks[16].y]
        
        # Usa o ângulo do braço esquerdo para a análise
        angle = calculate_angle((shoulder_left[0], shoulder_left[1]), (elbow_left[0], elbow_left[1]), (wrist_left[0], wrist_left[1]))
        
        # --- LÓGICA DE PROGRESSO E CONTAGEM ---
        progress = np.interp(angle, [self.angle_min, self.angle_max], [100, 0])

        if angle > self.angle_max: # Braços esticados
            if self.stage == 'down':
                self.feedback = "Excelente! Prepare para a próxima."
            self.stage = "up"
        elif angle < self.angle_min and self.stage == 'up': # Peito próximo ao chão
            self.stage = "down"
            self.counter += 1
            self.feedback = "Suba com força!"
        
        # Agrupa os marcos relevantes para facilitar o desenho na interface
        landmarks_to_draw = {
            "shoulder_left": shoulder_left,
            "elbow_left": elbow_left,
            "wrist_left": wrist_left,
            "shoulder_right": shoulder_right,
            "elbow_right": elbow_right,
            "wrist_right": wrist_right,
        }
        
        return self.counter, angle, self.stage, self.feedback, landmarks_to_draw, progress
