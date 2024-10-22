from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)
