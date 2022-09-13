from django.utils import timezone

from rest_framework import serializers, status

from pages.models import Page, Tag
from posts.serializers import PostDetailSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class PageSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Page
        fields = (
            "uuid", "name", "description", "image_path", "is_private", "is_blocked_permanently", "tags",
            "owner", "followers", "follow_requests")
        read_only_fields = ("followers", "follow_requests")


class PageListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Page
        fields = ("uuid", "name", "description", "image_path", "is_private", "is_blocked_permanently",
                  "unblock_date", "tags", "owner", "followers", "follow_requests")
        read_only_fields = ("followers", "follow_requests")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.unblock_date:
            representation['unblock_date'] = instance.unblock_date.strftime("%d.%m.%Y %H:%M")
        return representation


class PageDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    posts = PostDetailSerializer(many=True)

    class Meta:
        model = Page
        fields = ("uuid", "name", "description", "image_path", "is_private", "is_blocked_permanently",
                  "unblock_date", "tags", "owner", "posts", "followers", "follow_requests")
        read_only_fields = ("followers", "follow_requests")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.unblock_date:
            representation['unblock_date'] = instance.unblock_date.strftime("%d.%m.%Y %H:%M")
        return representation


class AcceptFollowSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)


class BlockPageSerializer(serializers.Serializer):
    unblock_date = serializers.DateTimeField(input_formats=['%d.%m.%Y %H:%M'])

    def validate(self, data):
        unblock_date = data.get("unblock_date")

        if unblock_date <= timezone.now():
            raise serializers.ValidationError("Unblock date is overdue", status.HTTP_400_BAD_REQUEST)

        return data
