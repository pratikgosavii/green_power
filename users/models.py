from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_showroom = models.BooleanField(default=False)
    is_distributor = models.BooleanField(default=False)
