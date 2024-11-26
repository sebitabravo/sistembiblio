from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    is_jefe_bodega = models.BooleanField(default=False)
    is_bodeguero = models.BooleanField(default=False)
