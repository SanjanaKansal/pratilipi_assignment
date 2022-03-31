from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from user import exceptions


def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        raise exceptions.UserDoesNotExistException


def get_user_by_username(username):
    try:
        return User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise exceptions.UserDoesNotExistException


def save_user(username, password):
    return User.objects.create(username=username, password=password)
