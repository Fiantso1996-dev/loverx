# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts' # Namespace pour accounts

urlpatterns = [
    # Inscription
    path('inscription/', views.register_view, name='register'),
    
    # Connexion (Utilise la vue intégrée de Django)
    path('connexion/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    
    # Déconnexion (Utilise la vue intégrée de Django)
    path('deconnexion/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Modification du profil (gestion des données utilisateur, pas les données Profile)
    # path('profil/', views.user_profile_view, name='profil'), # Optionnel, peut être géré par 'profiles'
    
    # Gestion du mot de passe oublié (à développer plus tard)
    # path('reinitialisation-mot-de-passe/', ... ),
    # NOUVEAU FLUX DE RÉINITIALISATION PERSONNALISÉ
    path('reset-password/start/', views.password_reset_start_view, name='password_reset_start'), 
    path('reset-password/verify/', views.password_reset_verify_view, name='password_reset_verify'),
    path('reset-password/confirm/', views.password_reset_confirm_view, name='password_reset_confirm'),

    # NOUVEAU CHEMIN DE VÉRIFICATION
    path('verify/', views.verify_registration_view, name='verify_registration'),
]