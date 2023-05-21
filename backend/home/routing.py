from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from .consumers import TelegramConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/telegram/', TelegramConsumer.as_asgi()),
    ]),
})