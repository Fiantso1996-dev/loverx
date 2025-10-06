# pages/admin.py

from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Configuration de l'affichage du modèle ContactMessage dans l'interface Admin.
    """
    
    # 1. Champs affichés dans la liste des messages
    list_display = (
        'sujet', 
        'nom', 
        'email', 
        'date_envoi', 
        'traite'
    )
    
    # 2. Champs qui peuvent être utilisés pour filtrer la liste
    list_filter = (
        'traite', 
        'date_envoi'
    )
    
    # 3. Champs cliquables pour trier (comme les colonnes)
    search_fields = (
        'nom', 
        'email', 
        'sujet', 
        'message'
    )
    
    # 4. Champs qui peuvent être modifiés directement depuis la liste
    list_editable = (
        'traite',
    )
    
    # 5. Ordre des champs et affichage des détails lors de l'édition
    fieldsets = (
        (None, {
            'fields': ('nom', 'email', 'sujet'),
        }),
        ('Message', {
            'fields': ('message',),
        }),
        ('Statut', {
            'fields': ('traite', 'date_envoi',),
        }),
    )
    
    # Rendre le champ date_envoi en lecture seule car il est auto_now_add
    readonly_fields = (
        'date_envoi',
    )