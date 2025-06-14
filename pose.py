import mediapipe as mp
import cv2
import matplotlib.pyplot as plt

class pose():
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose_image = self.mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5, model_complexity=1)
        self.pose_video = self.mp_pose.Pose(static_image_mode=False, model_complexity=1, 
                                          min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mp_drawing = mp.solutions.drawing_utils

    def detectPose(self, image, pose, draw=False, display=False):
        output_image = image.copy()
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(imageRGB)
        
        if results.pose_landmarks and draw:
            self.mp_drawing.draw_landmarks(
                image=output_image, 
                landmark_list=results.pose_landmarks,
                connections=self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=3, circle_radius=3),
                connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(49, 125, 237), thickness=2, circle_radius=2)
            )

        if display:
            plt.figure(figsize=[22, 22])
            plt.subplot(121); plt.imshow(image[:, :, ::-1]); plt.title("Original Image"); plt.axis('off')
            plt.subplot(122); plt.imshow(output_image[:, :, ::-1]); plt.title("Output Image"); plt.axis('off')
        else:
            return output_image, results

    def checkPose_LRC(self, image, results, draw=False, display=False):
        horizontal_position = None
        height, width, _ = image.shape
        output_image = image.copy()
        line_y_position = height // 3  # 1/3 from top

        left_x = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].x * width)
        right_x = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].x * width)

        if right_x <= width // 2 and left_x <= width // 2:
            horizontal_position = 'Left'
        elif right_x >= width // 2 and left_x >= width // 2:
            horizontal_position = 'Right'
        elif right_x >= width // 2 and left_x <= width // 2:
            horizontal_position = 'Center'

        if draw:
            cv2.putText(output_image, horizontal_position, (5, line_y_position - 10), 
                       cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
            cv2.line(output_image, (width // 2, 0), (width // 2, height), (255, 255, 255), 2)

        if display:
            plt.figure(figsize=[10, 10])
            plt.imshow(output_image[:, :, ::-1]); plt.title("Output Image"); plt.axis('off')
        else:
            return output_image, horizontal_position

    def checkPose_JSD(self, image, results, MID_Y, draw=False, display=False):
        height, width, _ = image.shape
        output_image = image.copy()
        line_y_position = height // 3  # 1/3 from top

        left_y = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y * height)
        right_y = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y * height)
        actual_mid_y = abs(right_y + left_y) // 2

        lower_bound = MID_Y - 15
        upper_bound = MID_Y + 100

        if actual_mid_y < lower_bound:
            posture = 'Jumping'
        elif actual_mid_y > upper_bound:
            posture = 'Crouching'
        else:
            posture = 'Standing'

        if draw:
            cv2.putText(output_image, posture, (5, line_y_position - 50), 
                       cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
            cv2.line(output_image, (0, line_y_position), (width, line_y_position), (255, 255, 255), 2)

        if display:
            plt.figure(figsize=[10, 10])
            plt.imshow(output_image[:, :, ::-1]); plt.title("Output Image"); plt.axis('off')
        else:
            return output_image, posture