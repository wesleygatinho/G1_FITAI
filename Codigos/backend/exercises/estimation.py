import cv2
import mediapipe as mp


class PoseEstimator:
    def __init__(self):
        """
        Inicializa o modelo de deteção de pose da MediaPipe.
        """
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def estimate_pose(self, frame):
        """
        Processa um único frame para encontrar os marcos da pose.
        Retorna o objeto 'results' da MediaPipe.
        O frame deve estar no formato BGR.
        
        Nota: As funções de desenho de linhas foram removidas daqui, 
        pois a API deve apenas processar dados, não desenhar em imagens.
        """
        # Converte BGR para RGB para o processamento da MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False # Otimização de performance

        # Estima a pose
        results = self.pose.process(rgb_frame)
        
        rgb_frame.flags.writeable = True # Reverte
        
        return results

    def close(self):
        """Libera os recursos do modelo de pose."""
        self.pose.close()

