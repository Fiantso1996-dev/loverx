# profiles/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages # Pour les messages de succès
from django.conf import settings
from django.http import Http404

# Assurez-vous d'importer vos modèles et formulaires
from .models import Profile
from .forms import ProfileUpdateForm
from accounts.models import CustomUser 


@login_required
def profile_edit_view(request):
    """
    Permet à l'utilisateur de modifier son propre profil.
    """
    # 1. Récupérer le profil de l'utilisateur connecté
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        # Si, pour une raison quelconque, le profil n'existe pas, créez-le
        # (Cela ne devrait pas arriver si le signal post_save est configuré)
        profile = Profile.objects.create(utilisateur=request.user)

    # 2. Gérer la soumission du formulaire (POST)
    if request.method == 'POST':
        # IMPORTANT : Utilisez request.FILES pour gérer le téléchargement d'images
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            # Enregistre le profil (y compris le fichier image)
            form.save()
            
            # Ajoute un message de succès
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            
            # Redirige vers la page de détail du profil
            # CETTE LIGNE est la réponse HTTP attendue, et non un dictionnaire
            return redirect('profiles:profile_detail', pk=profile.pk)
        else:
            # S'il y a des erreurs, les messages.error sont inutiles car le formulaire
            # les affichera dans le template.
            # print(form.errors) # Décommenter pour le débogage
            pass

    # 3. Gérer l'affichage initial ou les erreurs de formulaire (GET)
    else:
        # Initialiser le formulaire avec les données existantes du profil
        form = ProfileUpdateForm(instance=profile)

    # 4. Rendre le template
    context = {
        'form': form,
        'page_title': 'Modifier mon Profil',
    }
    return render(request, 'profiles/edit_profile.html', context)


@login_required
def profile_detail_view(request, pk):
    """Affiche le profil détaillé d'un membre."""
    
    # 1. Récupérer le profil ou lever une erreur 404
    profile = get_object_or_404(Profile, pk=pk)
    
    context = {
        'profile': profile,
        'page_title': f"Profil de {profile.prenom}",
    }
    return render(request, 'profiles/profile_detail.html', context)
    
    
@login_required
def profile_list_view(request):
    """Affiche la liste de tous les profils, sauf celui de l'utilisateur actuel."""
    
    # Exclure le profil de l'utilisateur connecté
    profiles = Profile.objects.exclude(utilisateur=request.user).order_by('-utilisateur__date_joined')
    
    context = {
        'profiles': profiles,
        'page_title': 'Découvrez les Membres',
        'query': None,
    }
    return render(request, 'profiles/profile_list.html', context)


@login_required
def member_search_view(request):
    """Gère la recherche de membres par prénom ou email."""
    query = request.GET.get('q')
    profiles = Profile.objects.exclude(utilisateur=request.user)

    if query:
        # Filtrage par prénom ou par email de l'utilisateur lié
        profiles = profiles.filter(
            Q(prenom__icontains=query) |
            Q(utilisateur__email__icontains=query)
        ).order_by('-utilisateur__date_joined')

    context = {
        'profiles': profiles,
        'page_title': f'Résultats pour "{query}"',
        'query': query,
    }
    return render(request, 'profiles/profile_list.html', context)