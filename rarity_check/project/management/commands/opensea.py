import project.cache as cache
import project.constants as constants
from project.get_obj import get_token_obj, get_token_obj_os
from project.models import Project, TraitType, TraitValue, Token
import project.opensea as opensea
import project.rarity as rarity
from project.web3_api import getIPFSHash

from django.core.management.base import BaseCommand, CommandError
from pprint import pprint

class Command(BaseCommand):
    #  def add_arguments(self, parser):
        #  parser.add_argument('num_tokens', nargs=1, type=int)

    def handle(self, *args, **options):
        project = Project.objects.get(
                contract_address=constants.CONTRACT_ADDRESS)
        #  opensea.inputAllAssets(project)
        print(Token.objects.filter(project=project).count())

        # add token URL's
        #  rarity.addTokenURLs(project)
