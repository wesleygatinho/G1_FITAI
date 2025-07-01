"""
@file hammer_curl.py
@brief Contém a lógica de rastreamento e contagem para o exercício de Rosca Martelo.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""
import numpy as np
from .angle_calculation import calculate_angle

class HammerCurl:
    """Gerencia o estado, a contagem e o feedback para o exercício de rosca martelo.

    Esta classe utiliza os marcos de pose para calcular o ângulo do cotovelo,
    contar as repetições e fornecer feedback sobre a execução do movimento.

    Attributes:
        counter (int): Contador de repetições completas.
        stage (str): Estágio atual do exercício, podendo ser 'up' (subida) ou 'down' (descida).
        feedback (str): Mensagem de texto para orientar o usuário.
        angle_min (int): Ângulo mínimo do cotovelo para registrar a fase 'up'.
        angle_max (int): Ângulo máximo do cotovelo para registrar a fase 'down'.
    """
    def __init__(self):
        """Inicializa o rastreador do exercício de rosca martelo.

        Define os valores iniciais para o contador, estágio do movimento e os
        limites de ângulo que caracterizam a repetição.
        """
        self.counter = 0
        self.stage = "down"
        self.feedback = "Inicie o movimento"
        # Define os ângulos mínimo e máximo do movimento
        self.angle_min = 30
        self.angle_max = 160

    def track_hammer_curl(self, landmarks, frame_shape):
        """Processa os marcos de pose para rastrear uma repetição do exercício.

        Calcula o ângulo do cotovelo direito, atualiza o estágio do movimento,
        incrementa o contador de repetições e gera feedback para o usuário.

        :param (object) landmarks: O objeto de resultados do MediaPipe com os marcos da pose.
        :param (tuple) frame_shape: A forma (altura, largura) do quadro do vídeo (não utilizado diretamente aqui).
        :return (tuple): Uma tupla contendo (contador, ângulo, estágio, feedback, marcos, progresso).
        """
        # Extrai as coordenadas dos pontos relevantes para ambos os braços
        shoulder_left = [landmarks[12].x, landmarks[12].y]
        elbow_left = [landmarks[14].x, landmarks[14].y]
        wrist_left = [landmarks[16].x, landmarks[16].y]
        shoulder_right = [landmarks[11].x, landmarks[11].y]
        elbow_right = [landmarks[13].x, landmarks[13].y]
        wrist_right = [landmarks[15].x, landmarks[15].y]
        
        # Usa o ângulo do braço direito como referência principal para a lógica
        angle = calculate_angle((shoulder_right[0], shoulder_right[1]), (elbow_right[0], elbow_right[1]), (wrist_right[0], wrist_right[1]))
        
        # --- LÓGICA DE PROGRESSO E CONTAGEM ---
        # Interpola o ângulo para uma barra de progresso (0 a 100)
        progress = np.interp(angle, [self.angle_min, self.angle_max], [100, 0])

        # Lógica de transição de estágios
        if angle > self.angle_max: # Braço considerado esticado
            self.stage = "down"
        elif angle < self.angle_min and self.stage == 'down': # Braço contraído vindo da posição 'down'
            self.stage = "up"
            self.counter += 1
            self.feedback = "Desça de forma controlada"
            
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
