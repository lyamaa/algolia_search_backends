import algoliasearch_django as algoliasearch
from algoliasearch_django import AlgoliaIndex

from .models import Article


class ArticleIndex(AlgoliaIndex):
    """Index for Article model"""

    # ** fields to index if is_published is True
    name = "article"
    should_index = "is_published_indexing"
    fields = (
        "title",
        "description",
        "is_published",
        "tags_indexing",
        "category_indexing",
        "likes_count",
    )
    settings = {
        "searchableAttributes": [
            "title",
            "description",
            "tags_indexing",
            "category_indexing",
        ],
        "attributesForFaceting": [
            "title",
            "tags_indexing",
            "description",
            "category_indexing",
        ],
        "queryType": "prefixAll",
        # ** custom ranking rules with like_count
        "customRanking": [
            "desc(likes_count)",
        ],
        "advancedSyntax": True,
        "highlightPreTag": "<mark>",
        "highlightPostTag": "</mark>",
        "hitsPerPage": 15,
    }

    index_name = "articles"


algoliasearch.register(Article, ArticleIndex)
