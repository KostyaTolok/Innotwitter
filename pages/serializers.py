from rest_framework import serializers

from pages.models import Page, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class PageDetailSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Page
        fields = "__all__"
        read_only_fields = ["followers", "follow_requests"]


class PageListSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = TagSerializer(many=True)

    class Meta:
        model = Page
        fields = ["uuid", "name", "image_path", "is_private", "unblock_date", "owner", "tags"]