import cv2

from proc.fingers_detector_proc import HandDetector

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, img = cam.read()
        img = detector.find_hands(img, draw=True)
        cv2.imshow('Test hand detector', img)

        finger_status = detector.get_raised_fingers(img)
        print(finger_status)

        key = cv2.waitKey(100) & 0xFF
        if key == 13:  # Enter
            break
