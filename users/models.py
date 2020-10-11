from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    icon = models.ImageField(upload_to='image/icon/', null=True, blank=True)
