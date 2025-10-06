# profiles/forms.py

from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    """
    Formulaire pour la modification des informations du profil (nom, description, image, etc.).
    """
    class Meta:
        model = Profile
        # Champs que l'utilisateur est autorisé à modifier
        fields = [
            'image', 
            'prenom', 
            'nom', 
            'age', 
            'description', 
            'telephone', 
            'adresse', 
            'cin'
        ]
        
        # Étiquettes personnalisées pour les champs
        labels = {
            'image': 'Photo de Profil',
            'cin': 'CIN (Optionnel)',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Applique la classe Bootstrap 'form-control' à tous les champs
        for field_name, field in self.fields.items():
            if field_name != 'image': # Le champ FileInput (image) est stylisé différemment
                field.widget.attrs.update({'class': 'form-control'})