from django.core.management.base import BaseCommand, CommandError

from shortener.models import KirrURL

class Command(BaseCommand):
    """docstring for Command."""

    help = 'Refresh all KirrURL Shortcodes.'

    def add_arguments(self, parser):
        parser.add_argument('items', type=int)

    def handle(self, *args, **options):

        return KirrURL.custom_manager.refresh_shortcodes(items=options['items'])
