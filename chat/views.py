# chat/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q # Utilisez Q plutôt que models.Q (plus propre)
from django.conf import settings
from django.http import Http404, HttpResponse

from .models import Message
# Assurez-vous d'importer Profile et CustomUser
from profiles.models import Profile 
from accounts.models import CustomUser 


@login_required
def chat_room_view(request, user_id):
    """
    Affiche une conversation spécifique et gère l'envoi de nouveaux messages.
    """
    # 1. Récupérer l'autre utilisateur et son profil
    
    # S'assurer que l'utilisateur cible existe
    OtherUser = get_object_or_404(CustomUser, pk=user_id)
    
    # POINT DE CORRECTION CRITIQUE : Assurez-vous que le profil de l'autre utilisateur existe
    try:
        OtherProfile = OtherUser.profile
    except Profile.DoesNotExist:
        # Lève une 404 si l'utilisateur n'a pas de profil (comme nous l'avons discuté)
        # Ceci est la cause racine de votre NoReverseMatch si le profil manque.
        raise Http404("Le profil de l'interlocuteur est introuvable.")
    
    # 2. Gestion de l'envoi de message (méthode POST)
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        
        if contenu:
            Message.objects.create(
                expediteur=request.user,
                destinataire=OtherUser,
                contenu=contenu
            )
            # Redirige pour éviter la soumission multiple du formulaire
            return redirect('chat:chat_room', user_id=user_id)
        
    # 3. Récupérer tous les messages entre les deux utilisateurs (méthode GET)
    messages = Message.objects.filter(
        Q(expediteur=request.user, destinataire=OtherUser) |
        Q(expediteur=OtherUser, destinataire=request.user)
    ).order_by('date_envoi')
    
    # 4. Marquer les messages reçus comme 'lu'
    messages.filter(destinataire=request.user, statut='non_lu').update(statut='lu')
    
    # 5. Préparer le contexte
    context = {
        'messages': messages,
        'other_user_id': user_id,
        'other_user_profile': OtherProfile, # L'objet Profile est maintenant dans le contexte
        'page_title': f"Chat avec {OtherProfile.prenom}",
    }
    return render(request, 'chat/chat_room.html', context)
    
    
@login_required
def chat_list_view(request):
    """
    Liste les utilisateurs avec qui l'utilisateur a des conversations actives.
    (Logique simplifiée pour l'exemple)
    """
    # Récupérer l'ensemble des IDs des utilisateurs impliqués dans des conversations
    user_ids = Message.objects.filter(
        Q(expediteur=request.user) | Q(destinataire=request.user)
    ).values_list('expediteur_id', 'destinataire_id')

    # Créer un set d'IDs uniques (sauf l'utilisateur actuel)
    contact_ids = set()
    for exp_id, dest_id in user_ids:
        if exp_id != request.user.pk:
            contact_ids.add(exp_id)
        if dest_id != request.user.pk:
            contact_ids.add(dest_id)
    
    # Récupérer les profils correspondants pour l'affichage dans chat_list.html
    contacts_profiles = Profile.objects.filter(utilisateur__in=list(contact_ids)).order_by('-utilisateur__last_login')

    context = {
        'contacts': contacts_profiles,
        'page_title': "Mes Discussions",
    }
    return render(request, 'chat/chat_list.html', context)

# chat/views.py (Ajouter ces imports si manquants)
from django.http import JsonResponse
from django.core import serializers
from datetime import datetime

# ... (Vos autres vues)

@login_required
def get_new_messages(request, user_id):
    """
    Vue AJAX qui renvoie les nouveaux messages pour l'utilisateur spécifié.
    Elle attend 'last_message_id' dans les paramètres GET.
    """
    last_message_id = request.GET.get('last_message_id')
    
    # Assurez-vous que l'autre utilisateur existe
    OtherUser = get_object_or_404(CustomUser, pk=user_id)
    
    # 1. Définir le filtre de base (messages entre les deux utilisateurs)
    messages_query = Message.objects.filter(
        Q(expediteur=request.user, destinataire=OtherUser) |
        Q(expediteur=OtherUser, destinataire=request.user)
    )

    # 2. Filtrer par ID si un last_message_id est fourni
    if last_message_id:
        messages_query = messages_query.filter(pk__gt=last_message_id)

    # 3. Exécuter la requête et sérialiser les données
    new_messages = messages_query.order_by('date_envoi')

    # Conversion des objets Django en format JSON
    message_data = []
    for message in new_messages:
        message_data.append({
            'id': message.pk,
            'contenu': message.contenu,
            'expediteur_id': message.expediteur.pk,
            'date_envoi': message.date_envoi.strftime("%H:%M"),
            'is_sent_by_me': message.expediteur == request.user
        })

    return JsonResponse({'messages': message_data})

