from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    first_name = models.CharField(max_length=150,)
    last_name = models.CharField(max_length=150,)
    email = models.EmailField(max_length=254, unique=True)
    # is_subscribed = models.BooleanField(default=False)
    avatar = models.ImageField(
        'Аватар',
        upload_to='users_images',
        blank=True,
        default=None
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
