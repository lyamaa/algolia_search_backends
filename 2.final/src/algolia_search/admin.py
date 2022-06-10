from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from algolia_search.models import Article, Category, ArticleLike


class UserAdmin(UserAdmin):
    model = User
    list_display = (
        "username",
        "email",
        "is_staff",
        "is_active",
    )
    list_filters = (
        "username",
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    (
                        "is_active",
                        "is_superuser",
                    ),
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Advanced options", {"classes": ("collapse",), "fields": ("groups",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)


admin.site.register(Category, CategoryAdmin)


class ArticleLikeInline(admin.TabularInline):
    model = ArticleLike
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "get_tags",
        "likes_count",
        "is_published",
    ]
    search_fields = ["id", "title"]

    def get_tags(self, article):
        tags = [str(tag) for tag in article.tags.all()]
        return ", ".join(tags)

    inlines = [
        ArticleLikeInline,
    ]


admin.site.register(Article, ArticleAdmin)
