import random
import time
import cv2
import os


def detector_function(shared_value):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Initialize model
    model_path = os.path.join(base_path, "etc", "face_recognition_model.yml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(model_path)

    # Initialize detector
    detector_path = os.path.join(base_path, "etc", "haarcascade_frontalface_default.xml")
    detector = cv2.CascadeClassifier(detector_path)

    cam = cv2.VideoCapture(0)

    while True:
        data = {}
        # Detecting faces for n seconds
        sec = 3
        start_time = time.time()
        while True:
            _, img = cam.read()
            img = cv2.flip(img, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Face detection
            faces = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            for (x, y, w, h) in faces:
                # Face recognition
                label, confidence = recognizer.predict(gray[y:y + h, x:x + w])

                # Collect data to send to screen process
                if confidence >= 100:
                    label = 0
                if label not in data:
                    data[label] = [confidence]
                else:
                    data[label].append(confidence)

            current_time = time.time()
            delta = current_time - start_time
            if delta >= sec:
                break

        if len(data.keys()) == 0:
            shared_value.value = -1
            continue

        # Sending data to screen process
        avg_list = [(key, sum(values) / len(values)) for key, values in data.items()]
        filter_list = [item for item in avg_list if item[0] != 0]
        sorted_list = sorted(filter_list, key=lambda x: x[1], reverse=True)

        if len(sorted_list) != 0:
            best_match = sorted_list[0]
            if best_match[1] <= 90:
                most_label = best_match[0]
            else:
                most_label = 0
        else:
            most_label = 0

        shared_value.value = most_label
