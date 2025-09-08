from django.urls import path
from django.http import JsonResponse
from .views import RegisterView, UserListView,MessageListCreateView,ConversationListView

def test_view(request):
    return JsonResponse({"message":'Chat API is working!'})

urlpatterns = [
    path("test/",test_view,name="test"),
    path("register/", RegisterView.as_view(), name="register"),
    path("users/", UserListView.as_view(), name="user-list"),  # ✅ added
    path("messages/<int:user_id>/", MessageListCreateView.as_view(), name="message-list-create"),
    path("conversations/",ConversationListView.as_view(),name="conversation-list"),
]
