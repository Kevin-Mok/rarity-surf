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
                contract_address=constants.CONTRACT_ADDRESS,
                name=constants.PROJECT_NAME,
                max_supply=constants.MAX_SUPPLY,
                ipfs_hash=constants.IPFS_HASH,
                api_url=constants.API_URL,
                )
        project.save()
