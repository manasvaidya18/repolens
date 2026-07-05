from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    
    email = models.EmailField(unique=True)

    github_id = models.BigIntegerField(
    unique=True,
    null=True,
    blank=True,
    )
    github_username = models.CharField(
    max_length=255,
    unique=True,
    blank=True,
    null=True,
)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    def __str__(self):
        return self.email