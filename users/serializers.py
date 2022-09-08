from django.shortcuts import get_object_or_404
from rest_framework import serializers, status

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "image_path", "role", "title", "is_blocked")


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, user_data):
        username = user_data.get("username")
        password = user_data.get("password")

        user = get_object_or_404(User, username=username)

        if not user.check_password(password):
            raise serializers.ValidationError("Password is incorrect", status.HTTP_400_BAD_REQUEST)

        return user_data


class BlockUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)
