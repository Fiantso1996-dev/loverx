# site_rencontre/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Inclusion des URLs des applications
    path('', include('home.urls', namespace='home')),
    path('membres/', include('profiles.urls', namespace='profiles')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('', include('accounts.urls', namespace='accounts')), # Pour login/register
]

# Service des fichiers médias (images de profil) uniquement en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)