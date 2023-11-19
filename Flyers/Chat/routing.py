from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/<id:event_id>/', consumers.ChatConsumer.as_asgi()),
]
