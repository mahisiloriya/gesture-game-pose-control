import cv2
import pyautogui
from time import time
from pose import pose


class game():
    def __init__(self):
        self.pose = pose()
        self.game_started = False
        self.x_pos_index = 1  # Center position
        self.y_pos_index = 1  # Standing position
        self.counter = 0
        self.time1 = 0
        self.MID_Y = None
        self.num_of_frames = 15  # Increased frames for more stable start

    def move_LRC(self, LRC):
        if (LRC == 'Left' and self.x_pos_index != 0) or (LRC == 'Center' and self.x_pos_index == 2):
            pyautogui.press('left')
            self.x_pos_index -= 1
        elif (LRC == 'Right' and self.x_pos_index != 2) or (LRC == 'Center' and self.x_pos_index == 0):
            pyautogui.press('right')
            self.x_pos_index += 1

    def move_JSD(self, JSD):
        if JSD == 'Jumping' and self.y_pos_index == 1:
            pyautogui.press('up')
            self.y_pos_index += 1
        elif JSD == 'Crouching' and self.y_pos_index == 1:
            pyautogui.press('down')
            self.y_pos_index -= 1
        elif JSD == 'Standing' and self.y_pos_index != 1:
            self.y_pos_index = 1

    def play(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 960)
        cv2.namedWindow('Subway Surfers with Pose Detection', cv2.WINDOW_NORMAL)

        while True:
            ret, image = cap.read()
            if not ret:
                continue

            image = cv2.flip(image, 1)
            image_height, image_width, _ = image.shape
            line_y_position = image_height // 3  # 1/3 from top

            image, results = self.pose.detectPose(image, self.pose.pose_video, draw=self.game_started)

            if results.pose_landmarks:
                if self.game_started:
                    image, LRC = self.pose.checkPose_LRC(image, results, draw=True)
                    self.move_LRC(LRC)

                    if self.MID_Y:
                        image, JSD = self.pose.checkPose_JSD(image, results, self.MID_Y, draw=True)
                        self.move_JSD(JSD)
                else:
                    cv2.putText(image, '.', 
                              (5, line_y_position - 10), 
                              cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

                image, LRC = self.pose.checkPose_LRC(image, results)
                if LRC == 'Center':
                    self.counter += 1
                    if self.counter == self.num_of_frames and not self.game_started:
                        self.game_started = True
                        self.MID_Y = line_y_position
                        pyautogui.click(x=1300, y=800, button='left')
                else:
                    self.counter = 0
            else:
                self.counter = 0

            # # FPS counter
            # time2 = time()
            # if (time2 - self.time1) > 0:
            #     frames_per_second = 1.0 / (time2 - self.time1)
            #     cv2.putText(image, f'FPS: {int(frames_per_second)}', 
            #                (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
            # self.time1 = time2

            cv2.imshow("Subway Surfers with Pose Detection", image)
            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


game = game()
game.play()