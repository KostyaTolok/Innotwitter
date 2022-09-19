from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):

    email = models.EmailField(verbose_name="User email", unique=True)
    image = models.URLField(verbose_name="User image", max_length=200, null=True, blank=True)
    role = models.CharField(verbose_name="User role", max_length=9, choices=Roles.choices, default=Roles.USER)
    title = models.CharField(verbose_name="User title", max_length=80)
    is_blocked = models.BooleanField(verbose_name="User is blocked", default=False)

    def __str__(self):
        return self.email
