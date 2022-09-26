from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Username is not specified')
        if not email:
            raise ValueError('Email is not specified')

        user = self.model(
            username=username,
            email=email
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_staff = True
        user.role = Roles.ADMIN
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(verbose_name="User email", unique=True)
    image = models.URLField(verbose_name="User image", max_length=200, null=True, blank=True)
    role = models.CharField(verbose_name="User role", max_length=9, choices=Roles.choices, default=Roles.USER)
    title = models.CharField(verbose_name="User title", max_length=80)
    is_blocked = models.BooleanField(verbose_name="User is blocked", default=False)

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
