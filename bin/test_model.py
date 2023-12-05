import cv2
import os
from db.database import *


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
    _, img = cam.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Rozpoznawanie twarzy
        label, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        if confidence < 100:
            label_text = get_user_name(label)
            confidence_text = "  {0}%".format(round(100 - confidence))
        else:
            label_text = "I dont know who this is :)"
            confidence_text = "  {0}%".format(round(100 - confidence))

        # Wyświetlanie identyfikatora i pewności
        cv2.putText(img, label_text, (x - 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(img, confidence_text, (x + 5, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    # Wyświetlanie obrazu w oknie
    cv2.imshow('camera', img)

    # Obsługa klawiatury i warunek zakończenia programu
    key = cv2.waitKey(10) & 0xff
    if key == 27:  # Klawisz ESC
        break

# Zwolnij zasoby
cam.release()
cv2.destroyAllWindows()
