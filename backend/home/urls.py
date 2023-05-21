from django.urls import path

from .views import index, chat
app_name = "home"

urlpatterns = [
    path('', index, name="home"),
    path('chat/', chat, name="chat"),
    
]

