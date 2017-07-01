from django.core.management.base import BaseCommand, CommandError
from shortener.models import shortenerURL

class Command(BaseCommand):
    help = "Refreshes all shortenerURL shortcodes"

    def add_arguments(self, parser):
        parser.add_argument("--items", type=int)

    def handle(self, *args, **options):
        return shortenerURL.objects.refresh_shortcodes(items=options["items"])
