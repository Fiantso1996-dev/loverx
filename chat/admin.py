# chat/admin.py

from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    """
    Configuration de l'affichage du modèle Message dans l'interface d'administration.
    """
    # 1. Champs à afficher dans la liste des messages
    list_display = (
        'expediteur', 
        'destinataire', 
        'date_envoi', 
        'contenu_apercu'
    )
    
    # 2. Champs qui peuvent être utilisés pour filtrer la liste
    list_filter = (
        'date_envoi', 
        'expediteur', 
        'destinataire'
    )
    
    # 3. Champs qui peuvent être utilisés pour rechercher des messages
    search_fields = (
        'contenu', 
        'expediteur__email', 
        'destinataire__email'
    )
    
    # 4. Affichage détaillé du message (en lecture seule)
    readonly_fields = (
        'date_envoi',
    )

    # 5. Définition d'une méthode pour afficher un aperçu du contenu
    def contenu_apercu(self, obj):
        """Affiche les 50 premiers caractères du message."""
        return obj.contenu[:50] + ('...' if len(obj.contenu) > 50 else '')
        
    # Nom plus convivial pour la colonne dans la liste
    contenu_apercu.short_description = 'Contenu (Aperçu)'


# Enregistrement du modèle Message avec sa configuration personnalisée
admin.site.register(Message, MessageAdmin)