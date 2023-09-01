from django.contrib.auth.hashers import check_password, make_password
from app.models import User


class UserSvc:
    @classmethod
    def check_user_exists(cls, email):
        try:
            user = User.get_by_username(email)
            return None if not user else user
        except Exception as e:
            raise e

    @classmethod
    def check_password(cls, pwd, encoded):
        try:
            is_matched = check_password(pwd, encoded)
            return True if is_matched else False
        except Exception as e:
            raise e

    @classmethod
    def add_user(cls, firstname, lastname, email, password):
        try:
            user_ent = User()
            user_ent.first_name = firstname
            user_ent.last_name = lastname
            user_ent.email = email
            user_ent.password = make_password(password)
            user_ent.is_active = True
            user_ent.username = email
            user_ent.save()
            return user_ent
        except Exception as e:
            raise e
