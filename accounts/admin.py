# accounts/admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

# Récupérer le modèle d'utilisateur actif (CustomUser)
CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    """
    Définition de la classe Admin pour CustomUser.
    Utilise les formulaires personnalisés pour la création et la modification 
    dans l'interface d'administration.
    """
    # Spécifiez les formulaires à utiliser pour l'ajout et la modification
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
    # 1. Champs affichés dans la liste des utilisateurs (User List)
    list_display = (
        'email', 
        'username', # Gardez-le même s'il est facultatif, pour l'admin
        'is_staff', 
        'is_active',
        'date_joined'
    )
    
    # 2. Champs qui peuvent être utilisés pour filtrer la liste
    list_filter = (
        'is_staff', 
        'is_active',
        'is_superuser'
    )
    
    # 3. Champs qui peuvent être utilisés pour rechercher des utilisateurs
    search_fields = (
        'email', 
        'username'
    )
    
    # 4. Ordre des champs lors de la MODIFICATION (dans l'Admin)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    # 5. Ordre des champs lors de la CRÉATION d'un nouvel utilisateur (dans l'Admin)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'password2'),
        }),
    )
    
    # Force l'utilisation de l'email comme identifiant unique
    ordering = ('email',)


# Enregistrement du modèle CustomUser avec la configuration personnalisée
admin.site.register(CustomUser, CustomUserAdmin)