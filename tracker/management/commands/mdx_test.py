from django.core.management.base import BaseCommand, CommandError

import importlib
import doctest


class Command(BaseCommand):
    help = 'Test markdown extensions'


    def add_arguments(self, parser):
        parser.add_argument('ext_name', help='Markdown extension name')

    def handle(self, *args, **options):
        try:
            mod = importlib.import_module('tracker.mdx.mdx_%s' % options['ext_name'])
        except ImportError:
            print("Error: Extension '%s' not found" % options['ext_name'])
        doctest.testmod(mod)
