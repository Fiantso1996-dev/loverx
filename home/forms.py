# pages/forms.py

from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    """
    Formulaire basé sur le modèle ContactMessage pour la soumission
    des demandes des utilisateurs sur la page de contact.
    """
    class Meta:
        model = ContactMessage
        # Nous incluons tous les champs de l'utilisateur
        # sauf 'date_envoi' et 'traite' qui sont gérés automatiquement.
        fields = ['nom', 'email', 'sujet', 'message']
        
        # Personnalisation des widgets avec des classes Bootstrap
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre Nom Complet'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre Adresse Email'
            }),
            'sujet': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sujet de votre message'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Écrivez votre message ici...'
            }),
        }
        
        # Définition des libellés (Labels)
        labels = {
            'nom': 'Nom',
            'email': 'Email',
            'sujet': 'Sujet',
            'message': 'Message',
        }