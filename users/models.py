from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True, max_length=150)
    date_of_birth = models.DateField(default=None, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth', ]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
