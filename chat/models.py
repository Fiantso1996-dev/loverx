# chat/models.py

from django.db import models
from django.conf import settings

# Récupération du modèle CustomUser défini dans settings.py
User = settings.AUTH_USER_MODEL 

class Message(models.Model):
    # 1. Expéditeur et Destinataire
    expediteur = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='messages_envoyes'
    )
    destinataire = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='messages_recus'
    )
    
    # 2. Contenu et Statut
    contenu = models.TextField()
    
    STATUT_CHOICES = (
        ('lu', 'Lu'),
        ('non_lu', 'Non Lu'),
    )
    statut = models.CharField(
        max_length=10, 
        choices=STATUT_CHOICES, 
        default='non_lu'
    )
    
    # 3. Date
    date_envoi = models.DateTimeField(auto_now_add=True)
 

    class Meta:
        ordering = ('date_envoi',) # Affichage chronologique
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        # Assurez-vous d'ajouter la guillemet simple (') à la fin de la chaîne.
        return f"De {self.expediteur.email} à {self.destinataire.email} ({self.date_envoi.strftime('%H:%M')})"