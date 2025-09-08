from django.urls import re_path
from . import consumers  # we will create consumers.py soon

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<user1_id>\d+)/(?P<user2_id>\d+/$", consumers.ChatConsumer.as_asgi()),
]
