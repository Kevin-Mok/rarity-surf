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
            #  permalink
            #  name (token_id)
            #  image_url
            #  """
            #  assets.append({

                #  })
        #  pprint(assets)

        project = Project.objects.get(
                #  contract_address=constants.CONTRACT_ADDRESS)
                contract_address="0xf497253c2bb7644ebb99e4d9ecc104ae7a79187a")
        #  token_obj = get_token_obj(project, 0)
        #  token_obj.os_url = f"{rarity.OS_ASSETS_URL}/" + \
                #  f"{project.contract_address}/" + \
                #  f"{token_obj.number}/"
        #  token_obj.save()
        #  print(f"Set {token_obj} URL to {token_obj.os_url}.")
        rarity.addTokenURLs(project)
