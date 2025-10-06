# accounts/views.py

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
import random 

# Importez tous les formulaires nécessaires (y compris le nouveau VerificationForm)
from .forms import (
    CustomUserCreationForm,
    PasswordResetStartForm, 
    PasswordResetVerifyForm, 
    PasswordResetConfirmForm,
    EmailVerificationForm, # <--- NOUVEAU FORMULAIRE
)

# Récupérer le modèle d'utilisateur personnalisé
CustomUser = get_user_model()


def register_view(request):
    """
    Étape 1 Inscription : Crée l'utilisateur (INACTIF) et envoie le code de vérification.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Créer l'utilisateur mais NE PAS l'activer immédiatement
            user = form.save(commit=False)
            user.is_active = False # Définir is_active à False
            user.save()
            
            # --- Logique de vérification ---
            code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            
            # Stocker les informations dans la session pour la vérification
            request.session['unverified_user_id'] = user.pk
            request.session['verification_code'] = code
            
            # Envoi de l'e-mail
            subject = 'Loverx: Code de vérification de compte'
            message = f'Bienvenue sur Loverx ! Votre code de confirmation pour activer votre compte est : {code}.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)
            
            messages.info(request, "Un code de vérification a été envoyé à votre adresse email. Veuillez le saisir pour activer votre compte.")
            return redirect('accounts:verify_registration') # <--- Nouvelle URL de redirection
            
    else:
        form = CustomUserCreationForm()
        
    context = {
        'form': form,
        'page_title': 'Inscription'
    }
    return render(request, 'accounts/register.html', context)



def verify_registration_view(request):
    """
    Étape 2 Inscription : Gère la vérification du code à 6 chiffres.
    Utilise le template: accounts/verify_registration.html (À créer)
    """
    # 1. Vérifier si l'inscription est en cours
    user_id = request.session.get('unverified_user_id')
    verification_code = request.session.get('verification_code')
    
    if not user_id or not verification_code:
        messages.error(request, 'Processus d\'inscription incomplet ou session expirée. Veuillez vous réinscrire.')
        return redirect('accounts:register')

    user = get_object_or_404(CustomUser, pk=user_id)

    if request.method == 'POST':
        form = EmailVerificationForm(request.POST) # <--- Utilise le nouveau formulaire
        if form.is_valid():
            submitted_code = form.cleaned_data['code']
            
            if submitted_code == verification_code:
                # Code correct : Activation de l'utilisateur
                user.is_active = True
                user.save()
                
                # Nettoyer la session
                del request.session['unverified_user_id']
                del request.session['verification_code']
                
                messages.success(request, 'Compte vérifié avec succès ! Vous pouvez maintenant vous connecter.')
                return redirect('accounts:login')
            else:
                messages.error(request, 'Code de vérification incorrect. Veuillez réessayer.')
    
    else:
        form = EmailVerificationForm()
        
    context = {
        'form': form,
        'email': user.email,
        'page_title': 'Vérification du Compte'
    }
    return render(request, 'accounts/verify_registration.html', context)

# ----------------------------------------------------------------------
# NOUVEAU FLUX DE RÉINITIALISATION PERSONNALISÉ
# ----------------------------------------------------------------------

def password_reset_start_view(request):
    """
    Étape 1 : Demande de l'email et envoi du code de vérification.
    Utilise le template: accounts/password_reset_start.html
    """
    if request.method == 'POST':
        form = PasswordResetStartForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            try:
                user = CustomUser.objects.get(email=email)
                
                # 1. Générer le code à 6 chiffres
                code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                
                # 2. Stocker le code et l'email dans la session
                request.session['reset_email'] = email
                request.session['reset_code'] = code
                
                # 3. Envoyer le code par email
                subject = 'Loverx: Code de réinitialisation de mot de passe'
                message = f'Bonjour {user.username or user.email},\n\nVotre code de confirmation pour réinitialiser votre mot de passe est : {code}.\nCe code expirera bientôt. Si vous n\'avez pas demandé cette réinitialisation, veuillez ignorer cet email.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)
                
                messages.success(request, 'Un code de confirmation a été envoyé à votre adresse email. Vérifiez votre boîte de réception.')
                return redirect('accounts:password_reset_verify')
            
            except CustomUser.DoesNotExist:
                # Maintient la sécurité en ne confirmant pas l'existence du compte
                messages.error(request, 'Si cette adresse email est associée à un compte, un code y a été envoyé.')
                return redirect('accounts:password_reset_start')
    
    else:
        form = PasswordResetStartForm()
        
    return render(request, 'accounts/password_reset_start.html', {'form': form, 'page_title': 'Réinitialisation (1/3)'})


def password_reset_verify_view(request):
    """
    Étape 2 : Vérification du code reçu par email.
    Utilise le template: accounts/password_reset_verify.html
    """
    # Vérifier si l'utilisateur a initié le processus
    if 'reset_email' not in request.session or 'reset_code' not in request.session:
        messages.error(request, 'Session expirée. Veuillez recommencer la procédure de réinitialisation.')
        return redirect('accounts:password_reset_start')
        
    correct_code = request.session['reset_code']
    
    if request.method == 'POST':
        form = PasswordResetVerifyForm(request.POST)
        if form.is_valid():
            submitted_code = form.cleaned_data['code']
            
            if submitted_code == correct_code:
                # Succès : Code correct. Marque l'étape comme réussie.
                request.session['code_verified'] = True 
                messages.success(request, 'Code vérifié. Vous pouvez maintenant choisir un nouveau mot de passe.')
                return redirect('accounts:password_reset_confirm')
            else:
                messages.error(request, 'Le code de confirmation est incorrect. Veuillez réessayer.')
    
    else:
        form = PasswordResetVerifyForm()
        
    return render(request, 'accounts/password_reset_verify.html', {'form': form, 'page_title': 'Réinitialisation (2/3)'})


def password_reset_confirm_view(request):
    """
    Étape 3 : Définition et confirmation du nouveau mot de passe.
    Utilise le template: accounts/password_reset_confirm.html
    """
    # Vérifier si les étapes précédentes ont été complétées
    if 'reset_email' not in request.session or request.session.get('code_verified') != True:
        messages.error(request, 'Procédure de vérification manquante. Veuillez recommencer.')
        return redirect('accounts:password_reset_start')
        
    email = request.session['reset_email']
    user = get_object_or_404(CustomUser, email=email)
    
    if request.method == 'POST':
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            
            # 1. Mettre à jour le mot de passe de l'utilisateur
            user.set_password(new_password)
            user.save()
            
            # 2. Nettoyer les variables de session pour des raisons de sécurité
            if 'reset_email' in request.session: del request.session['reset_email']
            if 'reset_code' in request.session: del request.session['reset_code']
            if 'code_verified' in request.session: del request.session['code_verified']
            
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès ! Vous pouvez maintenant vous connecter.')
            return redirect('accounts:login')
        
    else:
        form = PasswordResetConfirmForm()
        
    return render(request, 'accounts/password_reset_confirm.html', {'form': form, 'page_title': 'Réinitialisation (3/3)'})

# Note : Si vous avez une vue de connexion (login_view), ajoutez-la ici si elle manque.