from rest_framework import serializers
from taggit.models import Tag


class ArticleLikeSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class AddTagToArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")
