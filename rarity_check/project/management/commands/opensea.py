import project.cache as cache
import project.constants as constants
from project.get_obj import get_token_obj
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
        #  assets = opensea.getAssetsAPI(0)
        #  cache.cache_json(assets, constants.ASSETS_FILE)
        #  raw_assets = cache.read_json(constants.ASSETS_RAW_FILE)
        #  assets = []
        #  for raw_asset in raw_assets:
            #  """
            #  name (token_id)
            #  permalink
            #  image_url
            #  traits
            #  """
            #  assets.append({
                #  "name": raw_asset["name"],
                #  "traits": raw_asset["traits"],
                #  "os_url": raw_asset["permalink"],
                #  "image_url": raw_asset[                "image_url"],
                #  })
        #  pprint(assets)

        # add token URL's
        project = Project.objects.get(
                contract_address=constants.CONTRACT_ADDRESS)
        rarity.addTokenURLs(project)
