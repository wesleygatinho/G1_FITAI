"""
@file estimation.py
@brief Contém a classe PoseEstimator para detectar marcos de pose em uma imagem.
@author André Luis Aguiar do Nascimento
@author Hugo Samuel de Lima Oliveira
@author Leonardo Sampaio Serra
@author Lucas Emanoel Amaral Gomes
@author Wesley dos Santos Gatinho
"""
import cv2
import mediapipe as mp

class PoseEstimator:
    """Encapsula a funcionalidade de detecção de pose do MediaPipe.

    Esta classe inicializa o modelo de detecção de pose do MediaPipe e fornece
    métodos para processar imagens e liberar recursos.

    Attributes:
        mp_pose: Referência estática para o módulo mp.solutions.pose.
        pose (mp.solutions.pose.Pose): A instância do objeto de detecção de pose.
    """
    def __init__(self):
        """Inicializa o estimador de pose.

        Configura o detector de pose do MediaPipe com confiança mínima de
        detecção e rastreamento de 0.5.
        """
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def estimate_pose(self, frame):
        """Processa um quadro de imagem para encontrar marcos de pose.

        Converte o quadro de BGR para RGB, o torna não gravável para otimizar o
        desempenho e, em seguida, executa a detecção de pose do MediaPipe.

        :param (numpy.ndarray) frame: O quadro da imagem no formato BGR a ser processado.
        :return (object): O objeto de resultados do MediaPipe contendo os marcos da pose detectados.
        """
        # Converte a imagem de BGR para RGB para o processamento do MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Otimização: marca a imagem como não gravável para passar por referência
        rgb_frame.flags.writeable = False

        # Executa a estimativa de pose
        results = self.pose.process(rgb_frame)
        
        # Reverte a flag para que a imagem possa ser desenhada posteriormente
        rgb_frame.flags.writeable = True
        
        return results

    def close(self):
        """Libera os recursos do objeto de pose.

        Chama o método close() do detector de pose do MediaPipe para limpar
        os recursos alocados.

        :return: None
        """
        self.pose.close()
