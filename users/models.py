import datetime
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = None
    last_name = None

    id = models.UUIDField(primary_key=True, default=uuid4(), editable=False)
    username = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.username
