import project.cache as cache
import project.constants as constants
from project.models import Project

from django.core.management.base import BaseCommand, CommandError
from pprint import pprint

class Command(BaseCommand):
    #  def add_arguments(self, parser):
        #  parser.add_argument('num_tokens', nargs=1, type=int)

    def handle(self, *args, **options):
        project = Project(
                contract_address='0xf497253c2bb7644ebb99e4d9ecc104ae7a79187a',
                name='the-sevens',
                max_supply=7000,
                ipfs_hash='QmRE9x8qTTRtvS3UxDtzMCVV9GJKBfD8TgUoym1ePireGU',
                api_url='',
                )
        project.save()
