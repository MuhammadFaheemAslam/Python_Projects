from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Set the email field as the primary field for authentication
    USERNAME_FIELD = 'email'

    # Since 'email' is the primary identifier, 'username' is not required for user creation
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
