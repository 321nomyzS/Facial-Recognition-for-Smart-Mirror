import os

from tinydb import TinyDB, Query
from os import path

# Create database
base_path = path.dirname(path.dirname(path.abspath(__file__)))
db_path = path.join(base_path, "db", "db.json")
db = TinyDB(db_path)

users_table = db.table('users')
photos_table = db.table('photos')


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def to_dict(self):
        return {'id': self.user_id, 'name': self.name}


class Photo:
    def __init__(self, photo_id, file_path, user_id):
        self.photo_id = photo_id
        self.file_path = file_path
        self.user_id = user_id

    def to_dict(self):
        return {'id': self.photo_id, 'file_path': self.file_path, 'user_id': self.user_id}


def add_user(name):
    user_id = len(users_table) + 1
    user = User(user_id, name)
    users_table.insert(user.to_dict())
    return user


def delete_user_and_photos(user_id):
    photos = get_user_photos(user_id)

    for photo in photos:
        os.remove(photo['file_path'])

    users_table.remove(Query().id == user_id)
    photos_table.remove(Query().user_id == user_id)

    user_folder_path = os.path.join(base_path, "data", str(user_id))
    os.rmdir(user_folder_path)


def add_photo(file_path, user_id):
    photo_id = len(photos_table) + 1
    photo = Photo(photo_id, file_path, user_id)
    photos_table.insert(photo.to_dict())
    return photo


def get_user_name(user_id):
    user = users_table.get(Query().id == user_id)
    return user['name'] if user else None


def get_user_photos(user_id):
    user_photos = photos_table.search(Query().user_id == user_id)
    return user_photos


def get_next_user_id():
    last_user = users_table.all()[-1] if users_table.all() else None
    if last_user:
        return last_user['id'] + 1
    else:
        return 1
