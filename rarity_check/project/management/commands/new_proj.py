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
                contract_address='0x495f947276749ce646f68ac8c248420045cb7b5e',
                name='bitz',
                max_supply=975,
                ipfs_hash='',
                api_url='',
                )
        project.save()
