# chat/routing.py
from django.urls import re_path
from . import views
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws//inbox/chatBox/(?P<user>\w+)/$',consumers.ChatConsumer.as_asgi())
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]