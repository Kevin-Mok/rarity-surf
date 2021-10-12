import project.cache as cache
import project.constants as constants
from project.models import Project, TraitType, TraitValue, Token
from project.web3_api import getIPFSHash

from django.core.management.base import BaseCommand, CommandError
from pprint import pprint

IPFS_URL_PREFIX = "https://ipfs.io/ipfs"

def get_trait_type_obj(project, trait_type):
    """Create or retrieve trait_type_obj from project with
    trait_type.
    """
    trait_type_obj = TraitType.objects.filter(project=project, 
            name=trait_type)
    if not trait_type_obj.exists():
        trait_type_obj = TraitType(project=project, name=trait_type)
        trait_type_obj.save()
        print(f"Added new trait {trait_type}.")
    else:
        trait_type_obj = trait_type_obj[0]
    return trait_type_obj

def get_trait_value_obj(trait_type_obj, trait_value):
    """Create or retrieve trait_value_obj with
    trait_type_obj and trait_value.
    """
    trait_value_obj = TraitValue.objects.filter(
            trait_type=trait_type_obj)
    if not trait_value_obj.exists():
        trait_value_obj = TraitValue(
                trait_type=trait_type_obj, name=trait_value)
        trait_value_obj.save()
        print(f"Added new trait value {trait_value}.")
    else:
        trait_value_obj = trait_value_obj[0]
    return trait_value_obj

#  def add_new_traits(project, attributes):
    #  for trait in attributes:
        #  trait_type = trait[constants.TRAIT_TYPE_KEY]
        #  trait_type_obj = get_trait_type_obj(project, trait_type)
        #  trait_value_obj = get_trait_value_obj(
                #  trait_type_obj, trait[constants.TRAIT_VALUE_KEY])
        #  print(trait_value_obj)

def get_trait_objs(project, trait):
    trait_type = trait[constants.TRAIT_TYPE_KEY]
    trait_type_obj = get_trait_type_obj(project, trait_type)
    trait_value_obj = get_trait_value_obj(
            trait_type_obj, trait[constants.TRAIT_VALUE_KEY])
    return trait_type_obj, trait_value_obj

def get_image_url(image_url):
    return (f"{IPFS_URL_PREFIX}/{getIPFSHash(image_url)}" 
            if image_url.startswith("ipfs")
            else image_url)
    
class Command(BaseCommand):
    #  def add_arguments(self, parser):
        #  parser.add_argument('num_tokens', nargs=1, type=int)

    def handle(self, *args, **options):
        master_json = cache.read_json(constants.MASTER_JSON_FILE)
        token = master_json["0"]
        attributes = token[constants.ATTRIBUTES_KEY]
        project = Project.objects.get(
                contract_address=constants.CONTRACT_ADDRESS)
        token = Token(
                project=project,
                number=0,
                image_url=get_image_url(token["image"])
                )
        token.save()
        for trait in attributes:
            token.traits.add(get_trait_objs(
                project, trait)[1])
        token.save()
