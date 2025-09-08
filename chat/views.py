from pyexpat.errors import messages
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer,MessageSerializer # import UserSerializer
from .models import Message
from django.db.models import Max,Q
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.functions import Greatest, Least

User = get_user_model()

# 🔹 Register API
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # anyone can register

# 🔹 User List API
class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # login required

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class=MessageSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        other_user_id=self.kwargs["user_id"]
        return Message.objects.filter(
            sender__in=[user.id,other_user_id],
            receiver__in=[user.id,other_user_id]
        ).order_by("timestamp")
    
    def perform_create(self,serializer):
        serializer.save(sender=self.request.user)

from rest_framework import generics, permissions
from rest_framework.response import Response
from django.db.models import Max, Q, F, Case, When
from .models import Message

class ConversationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user

        # Step 1: get the latest message per conversation
        last_message_ids = (
            Message.objects.filter(Q(sender=user) | Q(receiver=user))
            .annotate(
                user_min=Case(
                    When(sender__id__lt=F('receiver__id'), then=F('sender__id')),
                    default=F('receiver__id')
                ),
                user_max=Case(
                    When(sender__id__lt=F('receiver__id'), then=F('receiver__id')),
                    default=F('sender__id')
                )
            )
            .values('user_min','user_max')
            .annotate(last_msg_id=Max('id'))
            .values_list('last_msg_id', flat=True)
        )

        # Step 2: get message objects for these IDs
        messages = Message.objects.filter(id__in=last_message_ids).order_by('-timestamp')

        # Step 3: format the response
        data = []
        for msg in messages:
            other_user = msg.receiver if msg.sender == user else msg.sender
            data.append({
                "id": msg.id,
                "other_user_id": other_user.id,
                "other_username": other_user.username,
                "last_message": msg.content,
                "timestamp": msg.timestamp,
            })

        return Response(data)