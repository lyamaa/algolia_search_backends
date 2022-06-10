from sys import stdout

from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command("algolia_reindex")
        stdout.write("\n Done....\n")
