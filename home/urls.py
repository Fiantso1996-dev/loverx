# home/urls.py
from django.urls import path
from . import views

app_name = 'pages' # Namespace pour home

urlpatterns = [
    # Page d'accueil (URL: /)
    path('', views.home_view, name='accueil'),
    
    # Page de présentation / À propos (URL: /a-propos/)
    path('a-propos/', views.about_view, name='a_propos'),
    
    # Autres pages publiques si nécessaire

     # Liens de votre footer
    path('terms/', views.terms_view, name='terms'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('contact/', views.contact_view, name='contact'),
    path('faq/', views.faq_view, name='faq'), 
]