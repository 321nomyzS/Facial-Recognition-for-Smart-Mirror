import cv2
import mediapipe as mp
import time


class HandDetector:
    def __init__(self):
        self.results = None
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_number=0, draw=True):
        landmark_pos = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_number]
            for id, lm in enumerate(hand.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmark_pos.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return landmark_pos


def fingers_detector_function(shared_value):
    cam = cv2.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, img = cam.read()

        img = detector.find_hands(img, draw=False)
        finger_list = detector.find_position(img, draw=False)

        if len(finger_list) > 0:
            # https://developers.google.com/static/mediapipe/images/solutions/hand-landmarks.png

            # Handle thumb
            if finger_list[4][1] > finger_list[17][1]:
                fingers_status = [finger_list[3][1] < finger_list[4][1]]
            else:
                fingers_status = [finger_list[3][1] > finger_list[4][1]]

            # Handle rest fingers
            fingers_status += [finger_list[8][2] < finger_list[6][2], finger_list[12][2] < finger_list[10][2],
                               finger_list[16][2] < finger_list[14][2], finger_list[20][2] < finger_list[18][2]]

            fingers_status = list(map(int, fingers_status))
            shared_value.value = sum(fingers_status)




