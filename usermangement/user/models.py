from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Custom_user(AbstractUser):
    email = models.EmailField(unique=True)
    is_blocked = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']
