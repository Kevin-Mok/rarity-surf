import project.constants as constants
from project.get_obj import get_token_type_obj
import project.rarity as rarity
from project.models import Project, TraitType, TraitValue, Token

from django.core.management.base import BaseCommand, CommandError
from pprint import pprint

class Command(BaseCommand):
    def handle(self, *args, **options):
        #  project = Project.objects.get(
                #  contract_address=constants.CONTRACT_ADDRESS)
        project = Project.objects.get(name="The Sevens")
        #  project = Project.objects.get(name="Bitz")

        # update score stats
        #  rarity.addTraitValueStats(project)
        #  rarity.addTokenScores(project)
        #  rarity.addTokenRanks(project)
        #  rarity.addToolsRanks(project)
        rarity.getAvgDiscrepanciesDB(project)

        # check highest ranks
        #  for token_obj in Token.objects.filter(
                #  project=project)[:25]:
            #  print(f"{token_obj.rank}. #{token_obj.number} {token_obj.score}")

        # check token rank
        #  token_type = get_token_type_obj(project, "Pigz")
        #  token = Token.objects.get(project=project,
                #  token_type=token_type, number=34)
        #  print(token.rank)

        # check Bitz rank
        #  bitz_trait = get_token_type_obj(project, "Bitz")
        #  bitz = Token.objects.filter(project=project,
                #  token_type=bitz_trait)
        #  rank = 1
        #  for bit in bitz:
            #  if bit.number == 630:
                #  print(rank)
            #  else:
                #  rank += 1
