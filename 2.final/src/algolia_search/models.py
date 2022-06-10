from django.db import models
from django.db.models import Manager, QuerySet
from taggit.managers import TaggableManager
from treebeard.mp_tree import MP_Node

from django.contrib.auth import get_user_model

User = get_user_model()


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(MP_Node):
    class Meta:
        db_table = "categories"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=30)

    node_order_by = ["name"]

    def __str__(self):
        return f"Category: {self.name}"


class ArticleQuerySet(QuerySet):
    def update(self, **kwargs):
        super(ArticleQuerySet, self).update(**kwargs)


class CustomManager(Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)


class ArticleLike(TimeStamp):
    class Meta:
        db_table = "article_like"
        unique_together = ("user", "article")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(
        "Article", on_delete=models.CASCADE, related_name="likes_article"
    )


class Article(TimeStamp):
    class Meta:
        db_table = "articles"

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    tags = TaggableManager()
    likes = models.ManyToManyField(
        User, related_name="user_likes_article", through=ArticleLike, blank=True
    )

    objects = CustomManager()

    def __str__(self):
        return self.title

    def is_published_indexing(self):
        return self.is_published == True

    @property
    def likes_count(self):
        return int(self.likes.count())

    @property
    def tags_indexing(self):
        return [tag.name for tag in self.tags.all()]

    @property
    def category_indexing(self):
        return self.category.name
