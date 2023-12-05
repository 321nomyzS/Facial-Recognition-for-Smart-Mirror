from db.database import *
from train_model import train_model

user_id = input("Podaj id użytkownika do usunięcia: ")
delete_user_and_photos(int(user_id))
train_model()
