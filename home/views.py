# home/views.py
from django.shortcuts import render
from profiles.models import Profile

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm # <--- NOUVEL IMPORT

# Page d'accueil (Accès public)
def home_view(request):
    """Affiche la page d'accueil de Loverx."""
    nombre_de_profils = Profile.objects.all().count()
    nbr_mois = Profile.objects.filter(utilisateur__date_joined__month=10)

    context = {
        'page_title': 'Accueil - Find Your Match',
        'nbr_user': str(nombre_de_profils),
        'nbr_mois': len(nbr_mois)
        # D'autres données nécessaires à home.html
    }
    return render(request, 'home/home.html', context)

# Page "À propos" / Présentation (Accès public)
def about_view(request):
    """Affiche la page de présentation/À propos."""
    context = {
        'page_title': 'À Propos de Loverx',
    }
    return render(request, 'home/about.html', context)

# Remarque : about.html n'était pas dans la liste initiale de templates, 
# nous allons le créer ou utiliser une autre page publique. Utilisons 'home/about.html' pour l'instant.


def terms_view(request):
    """Vue pour les Conditions d'Utilisation."""
    return render(request, 'home/terms.html', {'page_title': 'Conditions d\'Utilisation'})

def privacy_view(request):
    """Vue pour la Politique de Confidentialité."""
    return render(request, 'home/privacy.html', {'page_title': 'Politique de Confidentialité'})

def contact_view(request):
    """
    Vue pour la page de Contact, gérant la soumission du formulaire.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Enregistre le message de contact dans la base de données
            form.save()
            
            # Ici, vous pourriez ajouter la logique d'envoi d'e-mail à l'administrateur
            # pour notifier un nouveau message.
            
            messages.success(request, 'Merci ! Votre message a été envoyé avec succès. Nous vous répondrons dans les plus brefs délais.')
            return redirect('home:contact') # Redirige vers la page de contact (ou une page de succès)
    else:
        # Affiche le formulaire vide
        form = ContactForm()
        
    context = {
        'page_title': 'Contactez-nous',
        'form': form, # Passe le formulaire au template
    }
    return render(request, 'home/contact.html', context)

def faq_view(request):
    """Vue pour la Foire Aux Questions."""
    # Vous pouvez passer une liste de questions/réponses au contexte si elles sont statiques
    faq_items = [
        {'q': "Comment puis-je m'inscrire sur Loverx ?", 
         'a': "Cliquez sur 'S'inscrire' en haut à droite. La création de compte est rapide et nécessite la vérification de votre email."},
        {'q': "Comment fonctionne l'algorithme de match ?", 
         'a': "Notre algorithme utilise les préférences, les intérêts et la localisation que vous avez définis pour vous proposer des profils compatibles."},
        {'q': "Puis-je changer ma photo de profil après l'inscription ?", 
         'a': "Oui, vous pouvez mettre à jour votre photo et les informations de votre profil à tout moment via la section 'Mon Compte'."},
        {'q': "Comment signaler un utilisateur ?", 
         'a': "Sur le profil de l'utilisateur concerné, vous trouverez une option 'Signaler'. Nous prenons les signalements très au sérieux."},
        # Ajoutez plus de questions/réponses ici
    ]
    
    context = {
        'page_title': 'Foire Aux Questions (FAQ)',
        'faq_items': faq_items,
    }
    return render(request, 'home/faq.html', context)

# pages/views.py (Mise à jour pour contact_view)



