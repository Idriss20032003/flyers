
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_photo = models.ImageField(
        verbose_name='Photo de profil', null=True)

# APRES MERGE : enlever USER / CONSIDERER USER DE BASE DE DJANGO ET AJOUTER TABLE UTILISATEUR
