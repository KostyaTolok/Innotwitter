from django.shortcuts import get_object_or_404
from rest_framework import serializers, status

from Innotwitter.services import get_image_url
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "image", "role", "title", "is_blocked")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.image:
            representation['image'] = get_image_url(instance.image)
        return representation


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


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, user_data):
        username = user_data.get("username")
        password = user_data.get("password")

        user = get_object_or_404(User, username=username)

        if not user.check_password(password):
            raise serializers.ValidationError("Password is incorrect", status.HTTP_400_BAD_REQUEST)

        return user_data


class BlockUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)


class UpdateUserInfoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_null=True, use_url=True, required=False, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'title', 'image')
