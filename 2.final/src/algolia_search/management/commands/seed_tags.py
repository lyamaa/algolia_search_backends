from random import randrange
from sys import stdout

from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand, call_command
from faker import Faker
from taggit.models import Tag, TaggedItem

from algolia_search.models import Article


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()
        stdout.write("\n creating tags...waiting....\n")
        content_type = ContentType.objects.get_for_model(Article)
        for _ in range(randrange(len(Article.objects.all()))):
            Tag.objects.create(
                name=faker.unique.word(),
                slug=faker.unique.slug(),
            )
        tags = Tag.objects.all()
        # check if tag has already create if created then skip
        for instance in Article.objects.all():
            for tag in tags:
                if TaggedItem.objects.filter(
                    content_type=content_type,
                    object_id=instance.id,
                    tag=tag,
                ).exists():
                    continue
                instance.tags.add(tag)
