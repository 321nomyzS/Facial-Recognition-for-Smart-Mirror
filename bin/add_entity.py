import cv2
from db.database import *
from hashlib import sha256
from os import makedirs


def add_entity(user_name):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    detector_path = os.path.join(base_path, "etc", "haarcascade_frontalface_default.xml")
    detector = cv2.CascadeClassifier(detector_path)
    cam = cv2.VideoCapture(0)

    # Add new user to db
    user = add_user(user_name)
    user_id = user.user_id

    # Create user folder
    user_directory_path = os.path.join(base_path, "data", str(user_id))
    makedirs(user_directory_path, exist_ok=True)

    i = 0
    while True:
        _, img = cam.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            # Saving image
            cropped_image = gray[y:y + h, x:x + w]
            hash_object = sha256(cropped_image.tobytes())
            image_hash = hash_object.hexdigest()
            image_path = f"{user_directory_path}/{image_hash}.jpg"
            cv2.imwrite(image_path, cropped_image)

            # Add image to db
            add_photo(image_path, user_id)

            # Showing image
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.imshow('image', img)
            i += 1

        key = cv2.waitKey(100) & 0xFF
        if key == 13:  # Enter
            break
        elif i >= 30:
            break


if __name__ == '__main__':
    name = input("Write new user name: ")
    add_entity(name)
