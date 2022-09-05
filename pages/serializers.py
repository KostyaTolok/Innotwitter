from abc import ABC

from rest_framework import serializers

from pages.models import Page, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class PageSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Page
        fields = ("uuid", "name", "description", "image_path", "is_private", "unblock_date", "tags", "owner",
                  "followers", "follow_requests")
        read_only_fields = ("followers", "follow_requests")


class PageDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Page
        fields = ("uuid", "name", "description", "image_path", "is_private", "unblock_date", "tags", "owner",
                  "followers", "follow_requests")
        read_only_fields = ("followers", "follow_requests")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.unblock_date:
            representation['unblock_date'] = instance.unblock_date.strftime("%d.%m.%Y %H:%M")
        return representation


class AcceptFollowSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)
