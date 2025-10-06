# pages/models.py

from django.db import models

class ContactMessage(models.Model):
    """
    Modèle pour stocker les messages envoyés par les utilisateurs
    via le formulaire de la page de contact.
    """
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom complet"
    )
    email = models.EmailField(
        verbose_name="Adresse Email"
    )
    sujet = models.CharField(
        max_length=200,
        verbose_name="Sujet du message"
    )
    message = models.TextField(
        verbose_name="Contenu du message"
    )
    date_envoi = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'envoi"
    )
    traite = models.BooleanField(
        default=False,
        verbose_name="Traité (par l'administrateur)"
    )

    class Meta:
        verbose_name = "Message de Contact"
        verbose_name_plural = "Messages de Contact"
        ordering = ['-date_envoi']

    def __str__(self):
        return f"[{'Traité' if self.traite else 'Nouveau'}] {self.sujet} de {self.nom}"