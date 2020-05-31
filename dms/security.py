from werkzeug.security import safe_str_cmp
from .models.users import UsersModel


def authenticate(email_address, password):
    user = UsersModel.find_by_email_address(email_address)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload["identity"]
    return UsersModel.find_by_id(user_id)
