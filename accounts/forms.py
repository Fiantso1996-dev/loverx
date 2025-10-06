# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire pour la création de l'utilisateur. 
    Utilise l'email comme identifiant unique.
    """
    class Meta:
        # Utilise notre CustomUser
        model = CustomUser
        # Champs requis pour l'inscription : email et mot de passe (password1, password2)
        fields = ('email', 'username')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rend l'email le champ principal et masque potentiellement le 'username'
        # ou le rend non requis si le backend d'authentification est configuré pour l'utiliser comme un simple placeholder.
        # Dans ce cas, nous le gardons mais nous le rendons optionnel.
        self.fields['username'].required = False
        
        # Ajout d'attributs HTML pour le style Bootstrap (optionnel)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class CustomUserChangeForm(UserChangeForm):
    """
    Formulaire pour la modification des données de l'utilisateur par l'admin.
    """
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'is_active', 'is_staff')


# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model

# Récupérer le modèle d'utilisateur personnalisé
CustomUser = get_user_model()


# --- FORMULAIRES D'AUTHENTIFICATION DE BASE (Exemples) ---

class CustomUserCreationForm(UserCreationForm):
    """Formulaire pour l'inscription d'un nouvel utilisateur."""
    class Meta:
        model = CustomUser
        # Exclure 'username' si vous utilisez l'email comme identifiant principal
        fields = ('email', 'username',) 

class CustomUserChangeForm(UserChangeForm):
    """Formulaire pour la modification des données utilisateur (dans l'Admin)."""
    class Meta:
        model = CustomUser
        fields = ('email', 'username',)


# --- FORMULAIRES DE RÉINITIALISATION DE MOT DE PASSE PERSONNALISÉS ---

class PasswordResetStartForm(forms.Form):
    """Étape 1 : Demande de l'email pour initier la réinitialisation."""
    email = forms.EmailField(
        label="Adresse Email",
        max_length=254,
        widget=forms.EmailInput(attrs={'placeholder': 'Entrez votre email', 'class': 'form-control'})
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        # Vérifiez que l'utilisateur existe avant de continuer
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Cette adresse email n'est associée à aucun compte. "
                "Veuillez réessayer ou vous inscrire."
            )
        return email


class PasswordResetVerifyForm(forms.Form):
    """Étape 2 : Vérification du code à 6 chiffres."""
    code = forms.CharField(
        label="Code de Confirmation (6 chiffres)",
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'placeholder': '######', 
            'class': 'form-control form-control-lg text-center fw-bold',
            'pattern': '[0-9]{6}', # Assure que seuls les nombres sont saisis
            'title': 'Veuillez entrer le code de 6 chiffres reçu par email'
        })
    )


class PasswordResetConfirmForm(forms.Form):
    """Étape 3 : Définition et confirmation du nouveau mot de passe."""
    new_password1 = forms.CharField(
        label="Nouveau mot de passe", 
        widget=forms.PasswordInput(attrs={'placeholder': 'Nouveau mot de passe', 'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label="Confirmer le mot de passe", 
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer le nouveau mot de passe', 'class': 'form-control'})
    )

    def clean(self):
        """Vérifie que les deux mots de passe correspondent."""
        cleaned_data = super().clean()
        pwd1 = cleaned_data.get("new_password1")
        pwd2 = cleaned_data.get("new_password2")
        
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas. Veuillez les saisir à nouveau.")
        
        # Vous pouvez ajouter ici des validations de complexité si nécessaire
        
        return cleaned_data
    

class EmailVerificationForm(forms.Form):
    """Formulaire pour la saisie du code de vérification d'inscription."""
    code = forms.CharField(
        label="Code de Vérification Email (6 chiffres)",
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'placeholder': '######', 
            'class': 'form-control form-control-lg text-center fw-bold',
            'pattern': '[0-9]{6}', 
        })
    )