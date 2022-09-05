from rest_framework import serializers

from pages.models import Page, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class PageSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Page
        fields = "__all__"
        read_only_fields = ["followers", "follow_requests"]


class PageDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Page
        fields = "__all__"
        read_only_fields = ["followers", "follow_requests"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.unblock_date:
            representation['unblock_date'] = instance.unblock_date.strftime("%d.%m.%Y %H:%M")
        return representation
