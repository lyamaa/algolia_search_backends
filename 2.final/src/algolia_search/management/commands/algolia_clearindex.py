from sys import stdout

from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command("algolia_clearindex")
        stdout.write("\n Done....\n")
