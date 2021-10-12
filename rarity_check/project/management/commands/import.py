import project.cache as cache
import project.constants as constants
from project.get_obj import get_token_obj
from project.models import Project, TraitType, TraitValue, Token
from project.web3_api import getIPFSHash

from django.core.management.base import BaseCommand, CommandError
from pprint import pprint

class Command(BaseCommand):
    #  def add_arguments(self, parser):
        #  parser.add_argument('num_tokens', nargs=1, type=int)

    def handle(self, *args, **options):
        master_json = cache.read_json(constants.MASTER_JSON_FILE)
        project = Project.objects.get(
                contract_address=constants.CONTRACT_ADDRESS)
        for token_id in range(constants.MAX_SUPPLY):
            print(get_token_obj(project, token_id,
                master_json[str(token_id)]))
