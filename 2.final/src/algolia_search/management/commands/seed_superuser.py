"""
This script taken and modified from:
https://gist.github.com/c00kiemon5ter/7806c1eac8c6a3e82f061ec32a55c702
Extend createsuperuser command to allow non-interactive creation of a
superuser with a password.
Instructions:
  mkdir -p path-to-your-app/management/commands/
  touch path-to-your-app/management/__init__.py
  touch path-to-your-app/management/commands/__init__.py
and place this file under path-to-your-app/management/commands/
Example usage:
  manage.py seed_superuser \
          --password foo     \
          --email foo@foo.foo
"""
import os

from django.contrib.auth import get_user_model
from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError

User = get_user_model()


class Command(createsuperuser.Command):
    help = "Create a superuser with a password non-interactively"

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            "--password",
            dest="password",
            default=None,
            help="Specifies the password for the superuser.",
        )

    def handle(self, *args, **options):
        options.setdefault("interactive", False)
        database = options.get("database")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")

        if not password or not username:
            raise CommandError("--username and --password are required options")

        if User.objects.filter(username=username).count() > 0:
            self.stdout.write(
                self.style.SUCCESS("Superuser already seeded. Not seeding again.")
            )
            return

        user_data = {
            "password": password,
            "username": username,
            "email": email,
        }

        self.UserModel._default_manager.db_manager(database).create_superuser(
            **user_data
        )

        if options.get("verbosity", 0) >= 1:
            self.stdout.write(self.style.SUCCESS("Superuser seeded successfully."))
            return
