import project.cache as cache
import project.constants as constants
import project.get_obj as get_obj
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

        for token_id in range(7000):
            #  print(get_token(
                #  project, token_id, master_json[str(token_id)]))
            #  get_token(project, token_id, master_json[str(token_id)])
            print(get_obj.get_token_obj(
                project, token_id, master_json[str(token_id)]))
