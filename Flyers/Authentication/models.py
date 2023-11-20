
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


#class User(AbstractUser):
#    profile_photo = models.ImageField(
#        verbose_name='Photo de profil', null=True)

class Utilisateur(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client')
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField()

