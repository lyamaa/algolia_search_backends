from random import randrange
from sys import stdout

from django.core.management import BaseCommand, call_command
from faker import Faker

from django.contrib.auth import get_user_model

User = get_user_model()

#  hash password
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()
        stdout.write("\n creating user....\n")

        for _ in range(randrange(1, 10)):
            User.objects.create(
                username=faker.user_name(),
                email=faker.email(),
                password=make_password("123456"),
                is_active=True,
                is_superuser=False,
                is_staff=False,
            )
        stdout.write("\n Done....\n")
