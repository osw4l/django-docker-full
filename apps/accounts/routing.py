from django.urls import re_path
from . import consumers

auth2_websocket_urlpatterns = [
    re_path(r'ws/users/', consumers.UserStatusConsumer.as_asgi()),
]