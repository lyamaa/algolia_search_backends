from random import randrange
from sys import stdout

from django.core.management import BaseCommand, call_command
from faker import Faker

from algolia_search.models import Article, Category, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command("loaddata", "fixtures/Category.json")
        faker = Faker()
        stdout.write("\n creating....\n")
        categories = Category.objects.all()

        for _ in range(randrange(1, 30)):
            for i in range(len(categories)):
                Article.objects.create(
                    title=faker.sentence(),
                    description=faker.text(),
                    category=list(categories)[i],
                    is_published=randrange(0, 2),
                )
        call_command("seed_tags")
        stdout.write("\n Done....\n")
