from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    class Meta:
        db_table = "users"

    nickname = models.CharField(max_length=256, default='')