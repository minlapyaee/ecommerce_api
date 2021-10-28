from django.db import models
from django.contrib.auth.models import AbstractUser
import string
import random


def generate_unique_code():
    length = 6

    while True:
        item_code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if User.objects.filter(item_code=item_code).count() == 0:
            break

    return item_code


class User(AbstractUser):
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    item_code = models.CharField(
        max_length=8, default=generate_unique_code, unique=True)
    username = None
    last_login = None
    is_superuser = None
    first_name = None
    last_name = None
    is_staff = None
    is_active = None

    # django usually login with username so changed to email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
