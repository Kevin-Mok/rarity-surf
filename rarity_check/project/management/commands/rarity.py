import project.constants as constants
import project.rarity as rarity
from project.models import Project, TraitType, TraitValue, Token

from django.core.management.base import BaseCommand, CommandError
from pprint import pprint

class Command(BaseCommand):
    def handle(self, *args, **options):
        project = Project.objects.get(
                contract_address=constants.CONTRACT_ADDRESS)
        rarity.addTraitValueStats(project)
        #  rarity.addTokenScores(project)
        #  for token_obj in Token.objects.all()[:7]:
            #  print(token_obj.number, token_obj.score)
