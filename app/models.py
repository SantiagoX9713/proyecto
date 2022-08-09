from flask_login import UserMixin
from .firebase_service import get_user


class UserData:
    def __init__(self, username, password, profile='common'):
        self.username = username
        self.password = password
        self.profile = profile


class UserModel(UserMixin):
    def __init__(self, user_data):
        self.id = user_data.username
        self.password = user_data.password
        self.profile = user_data.profile


    @staticmethod
    def query(user_id):
        user_doc = get_user(user_id)
        user_data = UserData(user_doc.id, user_doc.to_dict()['password'], user_doc.to_dict()['profile'])
        return UserModel(user_data)
