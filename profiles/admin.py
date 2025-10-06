# profiles/admin.py

from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    """
    Configuration de l'affichage du modèle Profile dans l'interface d'administration.
    """
    # 1. Champs à afficher dans la liste des profils
    list_display = (
        'utilisateur_email', 
        'prenom', 
        'age', 
        'telephone', 
        'image_apercu'
    )
    
    # 2. Champs qui peuvent être utilisés pour filtrer la liste
    list_filter = (
        'age',
        'adresse', 
        'utilisateur__is_active',
    )
    
    # 3. Champs qui peuvent être utilisés pour rechercher des profils
    search_fields = (
        'prenom', 
        'nom', 
        'utilisateur__email', # Permet de rechercher par email de l'utilisateur lié
        'description'
    )
    
    # 4. Ordre des champs lors de la MODIFICATION (dans l'Admin)
    fieldsets = (
        ('Lien Utilisateur', {'fields': ('utilisateur',)}),
        ('Informations de Base', {'fields': ('prenom', 'nom', 'date_naissance', 'age', 'telephone', 'cin', 'adresse')}),
        ('Contenu et Média', {'fields': ('description', 'image', 'image_apercu')}),
    )

    # Rendre certains champs non éditables
    readonly_fields = ('age', 'image_apercu',) 
    
    # Méthodes personnalisées
    
    def utilisateur_email(self, obj):
        """Affiche l'email de l'utilisateur lié dans la liste."""
        return obj.utilisateur.email
    utilisateur_email.short_description = 'Email'
    
    def image_apercu(self, obj):
        """Affiche un aperçu miniature de l'image de profil."""
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />', obj.image.url)
        return "Pas d'image"
    image_apercu.short_description = 'Photo'


# Enregistrement du modèle Profile avec sa configuration personnalisée
admin.site.register(Profile, ProfileAdmin)