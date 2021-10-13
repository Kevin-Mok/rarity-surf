import project.constants as constants
import project.rarity as rarity
from project.models import Project, TraitType, TraitValue, Token

from django.core.management.base import BaseCommand, CommandError
from pprint import pprint

class Command(BaseCommand):
    def handle(self, *args, **options):
        #  project = Project.objects.get(
                #  contract_address=constants.CONTRACT_ADDRESS)
        #  project = Project.objects.get(name="The Sevens")
        project = Project.objects.get(name="Bitz")
        #  rarity.addTraitValueStats(project)
        #  rarity.addTokenScores(project)
        for token_obj in Token.objects.filter(project=project)[:7]:
            #  print(token_obj.number, token_obj.score)
            print(token_obj)
            #  print(token_obj.token_type)
