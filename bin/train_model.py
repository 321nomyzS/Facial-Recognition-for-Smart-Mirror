import cv2
import numpy as np
from PIL import Image
import os


def detect_faces_on_images():
    faces_objects = []
    labels = []

    # Create path to files
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_path, "data")

    # Detector
    detector_path = os.path.join(base_path, "etc", "haarcascade_frontalface_default.xml")
    detector = cv2.CascadeClassifier(detector_path)

    for user_id in os.listdir(data_path):
        user_path = os.path.join(data_path, user_id)

        # Check if user_path is dir
        if not os.path.isdir(user_path):
            continue

        for image_file in os.listdir(user_path):
            image_path = os.path.join(user_path, image_file)
            image_object = Image.open(image_path).convert('L')
            image_numpy = np.array(image_object, 'uint8')
            faces = detector.detectMultiScale(image_numpy)

            for (x, y, w, h) in faces:
                faces_objects.append(image_numpy[y:y + h, x:x + w])
                labels.append(int(user_id))

    return faces_objects, labels


def train_model():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Detect faces on images
    faces, labels = detect_faces_on_images()

    # Recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(labels))

    # Saving model
    model_path = os.path.join(base_path, "etc", "face_recognition_model.yml")
    recognizer.save(model_path)


if __name__ == "__main__":
    train_model()
    print("Model został pomyślnie wytrenowany i zapisany do pliku")
