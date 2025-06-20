# angle_calculation.py
import math

def calculate_angle(a, b, c):

    ba = [a[0] - b[0], a[1] - b[1]]
    bc = [c[0] - b[0], c[1] - b[1]]

    dot_product = ba[0] * bc[0] + ba[1] * bc[1]

    magnitude_ba = math.sqrt(ba[0]**2 + ba[1]**2)
    magnitude_bc = math.sqrt(bc[0]**2 + bc[1]**2)

    if magnitude_ba == 0 or magnitude_bc == 0:
        return 0

    cosine_angle = dot_product / (magnitude_ba * magnitude_bc)

    cosine_angle = max(min(cosine_angle, 1.0), -1.0)
    
    angle = math.degrees(math.acos(cosine_angle))
    return angle

# estimation.py
import cv2
import mediapipe as mp

class PoseEstimator:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def estimate_pose(self, frame):
        """
        Processes a single frame to find pose landmarks.
        Returns the results object from MediaPipe.
        The frame should be in BGR format.
        """
        # BGR to RGB for MediaPipe processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False # Performance optimization

        # Pose estimation
        results = self.pose.process(rgb_frame)
        
        rgb_frame.flags.writeable = True # Revert back
        
        return results

    def close(self):
        self.pose.close()

