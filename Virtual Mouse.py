import cv2
import mediapipe as mp
import pyautogui
import math
from enum import IntEnum

pyautogui.FAILSAFE = False
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


# Gesture Encodings
class Gest(IntEnum):
    PALM = 31
    PINCH_MAJOR = 35
    DOUBLE_FINGER = 36


class HandRecog:
    def __init__(self):
        self.hand_result = None

    def update_hand_result(self, hand_result):
        self.hand_result = hand_result

    def get_distance(self, index1, index2):
        if self.hand_result is None:
            return float('inf')
        x1, y1 = self.hand_result.landmark[index1].x, self.hand_result.landmark[index1].y
        x2, y2 = self.hand_result.landmark[index2].x, self.hand_result.landmark[index2].y
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def get_gesture(self):
        if self.hand_result is None:
            return Gest.PALM

        thumb_index = 4  # Thumb tip
        index_index = 8  # Index finger tip
        middle_index = 12  # Middle finger tip

        distance_thumb_index = self.get_distance(thumb_index, index_index)
        distance_index_middle = self.get_distance(index_index, middle_index)

        # Define thresholds for gestures
        pinch_threshold = 0.05  # For pinch gesture
        double_finger_threshold = 0.1  # For double finger gesture

        if distance_thumb_index < pinch_threshold:
            return Gest.PINCH_MAJOR  # Pinch gesture detected
        elif distance_index_middle < double_finger_threshold:
            return Gest.DOUBLE_FINGER  # Double finger gesture detected

        return Gest.PALM  # Default to palm


class Controller:
    pinch_started = False
    double_finger_started = False

    @staticmethod
    def get_position(hand_result):
        point = 9  # Index finger tip
        position = [hand_result.landmark[point].x, hand_result.landmark[point].y]
        sx, sy = pyautogui.size()
        x = int(position[0] * sx)
        y = int(position[1] * sy)
        return (x, y)

    @staticmethod
    def click_left():
        pyautogui.click()  # Left click

    @staticmethod
    def click_right():
        pyautogui.click(button='right')  # Right click


class HandGestureControl:
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        self.hand_recog = HandRecog()

    def start(self):
        with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8) as hands:
            while True:
                ret, frame = self.capture.read()
                if not ret:
                    continue

                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(frame_rgb)

                hand_landmarks = None

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.hand_recog.update_hand_result(hand_landmarks)
                        gesture = self.hand_recog.get_gesture()

                        # Get position for moving the cursor
                        new_pos = Controller.get_position(hand_landmarks)
                        pyautogui.moveTo(new_pos)

                        # Check for pinch gesture
                        if gesture == Gest.PINCH_MAJOR:
                            if not Controller.pinch_started:
                                Controller.pinch_started = True
                                Controller.click_left()  # Perform left click
                        else:
                            Controller.pinch_started = False  # Reset if not pinching

                        # Check for double finger gesture
                        if gesture == Gest.DOUBLE_FINGER:
                            if not Controller.double_finger_started:
                                Controller.double_finger_started = True
                                Controller.click_right()  # Perform right click
                        else:
                            Controller.double_finger_started = False  # Reset if not double finger

                        # Draw landmarks
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                cv2.imshow('Hand Gesture Control', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        self.capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    controller = HandGestureControl()
    controller.start()
