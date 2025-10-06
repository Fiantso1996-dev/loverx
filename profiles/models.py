# profiles/models.py

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Récupération du modèle CustomUser défini dans settings.py
User = settings.AUTH_USER_MODEL 

class Profile(models.Model):
    # 1. Clé étrangère vers l'utilisateur (relation 1:1)
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # 2. Champs du plan
    nom = models.CharField(max_length=50, blank=False)
    prenom = models.CharField(max_length=50, blank=False)
    adresse = models.CharField(max_length=255, blank=True)
    age = models.IntegerField(null=True, blank=True)
    description = models.TextField(max_length=500, blank=True)
    cin = models.CharField(max_length=20, blank=True, verbose_name="CIN (Carte d'Identité Nationale)")
    telephone = models.CharField(max_length=20, blank=True)
    
    # L'email est pris via utilisateur.email (pas besoin de le dupliquer ici)
    
    image = models.ImageField(
        upload_to='profile_pics', 
        default='profile_pics/default.png', # Optionnel : image par défaut
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Profil de {self.utilisateur.email}"

# Signal Django : Créer un profil automatiquement lors de l'inscription
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(utilisateur=instance)

# Signal Django : Sauvegarder le profil lors de la sauvegarde de l'utilisateur
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # Gère le cas où l'utilisateur a été créé sans profil
        Profile.objects.create(utilisateur=instance)