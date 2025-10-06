# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Rôles utilisateur
    ROLE_CHOICES = (
        ('utilisateur', 'Utilisateur'),
        ('administrateur', 'Administrateur'), # Optionnel
    )
    
    # 1. Champs du plan
    email = models.EmailField(unique=True, blank=False)
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='utilisateur'
    )
    # date_d_inscription est déjà géré par AbstractUser (date_joined)

    # 2. Remplacer le nom d'utilisateur par l'email pour la connexion
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # 'username' reste un champ requis par AbstractUser

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Utilisateur Loverx"
        verbose_name_plural = "Utilisateurs Loverx"