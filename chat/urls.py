# chat/urls.py
from django.urls import path
from . import views

app_name = 'chat' # Namespace pour chat

urlpatterns = [
    # Liste des discussions actives (URL: /chat/)
    path('', views.chat_list_view, name='chat_list'),
    
    # Conversation avec un utilisateur spécifique (URL: /chat/utilisateur-id/)
    path('<int:user_id>/', views.chat_room_view, name='chat_room'),
    path('messages/<int:user_id>/new/', views.get_new_messages, name='get_new_messages'),
    # path('delete-messages/', views.delete_message_view, name='delete_messages'),
    # Point d'API pour l'envoi de messages (si non temps réel)
    # path('envoyer-message/', views.send_message, name='send_message'),

   
]