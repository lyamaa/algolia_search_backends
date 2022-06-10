from algoliasearch.search_client import SearchClient
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Article
from taggit.models import Tag
from .serializers import AddTagToArticleSerializer, ArticleLikeSerializer

client = SearchClient.create(
    settings.ALGOLIA["APPLICATION_ID"], settings.ALGOLIA["API_KEY"]
)
index = client.init_index("articles")


def getArticles(request, query):
    return index.search(query)


class ArticleLikeView(APIView):
    """
    * id is required.
    {
        "id": 1, // article id
    }
    """

    def post(self, request, *args, **kwargs):
        serializer = ArticleLikeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            article_id = data.get("id")

            articles = Article.objects.filter(id=article_id)
            if not articles.exists():
                return Response({"msg": "Article not found"}, status.HTTP_404_NOT_FOUND)
            obj = articles.first()
            # ** check if the user has already liked the article
            #  ** if not, then like the article
            # ** elif, then unlike the article
            if request.user not in obj.likes.all():
                obj.likes.add(request.user)
                index.partial_update_object(
                    dict(objectID=obj.id, id=obj.id, likes_count=obj.likes.count())
                )
                return Response({"msg": "Article liked"}, status.HTTP_200_OK)
            elif request.user in obj.likes.all():
                obj.likes.remove(request.user)
                index.partial_update_object(
                    dict(objectID=obj.id, id=obj.id, likes_count=obj.likes.count()),
                )
                return Response({"msg": "Article unliked"}, status.HTTP_200_OK)

        return Response({"msg": "Something went wrong"}, status.HTTP_400_BAD_REQUEST)


class AddNewTagToArticle(APIView):
    """append new tag to article by logged in user"""

    def post(self, request, *args, **kwargs):
        serializer = AddTagToArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            article_id = request.data.get("id")
            name = request.data.get("name")
            name_split = name.split(",")
            articles = Article.objects.filter(id=article_id)
            obj = articles.first()

            if not obj.tags.filter(name=name).exists():
                try:
                    for i in name_split:
                        obj.tags.add(Tag.objects.create(name=i))
                    return Response({"msg": "Tag added"}, status.HTTP_200_OK)
                except Exception as e:
                    return Response({"msg": "Tag exists"}, status.HTTP_400_BAD_REQUEST)
            return Response({"msg": "Tag exists"}, status.HTTP_400_BAD_REQUEST)
