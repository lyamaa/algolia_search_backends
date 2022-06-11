from random import randrange
from sys import stdout

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from faker import Faker

from algolia_search.models import Article, ArticleLike

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()

        stdout.write("\n creating tags...waiting....\n")
        #  create article like should be unique
        for instance in User.objects.all():
            # check if user has already liked an article if liked then skip
            if ArticleLike.objects.filter(user=instance).exists():
                continue

            # create article like
            for obj in range(randrange(1, 10)):
                obj.likes.add(instance)

        stdout.write("\n Done....\n")
