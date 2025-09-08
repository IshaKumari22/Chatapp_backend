from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message,User

User = get_user_model()

# 🔹 For registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"]
        )
        return user

# 🔹 For user list
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]



class MessageSerializer(serializers.ModelSerializer):
    sender=serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    receiver=serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username"
    )
    class Meta:
        model=Message
        fields=["id","sender","receiver","content","timestamp"]