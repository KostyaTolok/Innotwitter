from rest_framework import serializers

from pages.serializers import PageDetailSerializer
from posts.models import Post
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("page", "content", "reply_to")


class PostDetailSerializer(serializers.ModelSerializer):
    likes = UserSerializer(many=True)

    class Meta:
        model = Post
        fields = ("page", "content", "reply_to", "likes", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = instance.created_at.strftime("%d.%m.%Y %H:%M")
        representation['updated_at'] = instance.updated_at.strftime("%d.%m.%Y %H:%M")
        return representation
