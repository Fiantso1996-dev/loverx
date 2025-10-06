# profiles/urls.py
from django.urls import path
from . import views

app_name = 'profiles' # Namespace pour profiles

urlpatterns = [
    # Liste de tous les profils (URL: /membres/)
    path('', views.profile_list_view, name='profile_list'),
    
    # Voir son propre profil ou celui d'un autre utilisateur
    # Ex: /membres/moi/ ou /membres/5/
    path('<int:pk>/', views.profile_detail_view, name='profile_detail'),
    
    # Modifier son profil (URL: /membres/modifier/)
    path('modifier/', views.profile_edit_view, name='profile_edit'),
    
    # Recherche de membres (URL: /membres/rechercher/)
    path('rechercher/', views.member_search_view, name='member_search'),
]