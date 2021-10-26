import project.constants as constants
from project.get_obj import get_token_type_obj, get_trait_objs, get_trait_type_obj
import project.rarity as rarity
from project.models import Project, TraitType, TraitValue, Token

from django.core.management.base import BaseCommand, CommandError
from pprint import pprint

class Command(BaseCommand):
    def handle(self, *args, **options):
        project = Project.objects.get(name="The Sevens")
        plain_trait = TraitValue.objects.get(name="No Aura Plain")
        no_aura_trait = TraitValue.objects.get(name="No Aura")
        plain_tokens = Token.objects.filter(project=project,
                traits=plain_trait)
        #  for token in plain_tokens:
            #  token.traits.add(no_aura_trait)
            #  token.traits.remove(plain_trait)
        #  plain_trait.delete()
        #  print(plain_tokens)
