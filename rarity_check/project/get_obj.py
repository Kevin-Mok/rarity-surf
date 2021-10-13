import project.cache as cache
import project.constants as constants
from project.models import Project, TraitType, TraitValue, TokenType, Token
from project.scrape import getTokenID 
from project.web3_api import getIPFSHash

from django.core.management.base import BaseCommand, CommandError
from pprint import pprint

IPFS_URL_PREFIX = "https://ipfs.io/ipfs"

def get_project_obj(contract_address, project_name):
    project_obj = Project.objects.filter(
            contract_address=contract_address,
            name=project_name)
    if not project_obj.exists():
        project_obj = Project(
                contract_address=contract_address,
                name=project_name,
                slug=constants.PROJECT_SLUG,
                max_supply=constants.MAX_SUPPLY,
                ipfs_hash=constants.IPFS_HASH,
                api_url=constants.API_URL)
        project_obj.save()
        print(f"Added new project {project_obj}.")
    else:
        project_obj = project_obj[0]
    return project_obj

def get_trait_type_obj(project, trait_type):
    """Create or retrieve trait_type_obj from project with
    trait_type.
    """
    trait_type_obj = TraitType.objects.filter(project=project, 
            name=trait_type)
    if not trait_type_obj.exists():
        trait_type_obj = TraitType(project=project, name=trait_type)
        trait_type_obj.save()
        print(f"Added new trait type {trait_type_obj}.")
    else:
        trait_type_obj = trait_type_obj[0]
        #  print(f"Existing trait type {trait_type_obj}.")
    return trait_type_obj

def get_trait_value_obj(trait_type_obj, trait_value):
    """Create or retrieve trait_value_obj with
    trait_type_obj and trait_value.
    """
    trait_value_obj = TraitValue.objects.filter(
            trait_type=trait_type_obj, name=trait_value)
    if not trait_value_obj.exists():
        trait_value_obj = TraitValue(
                trait_type=trait_type_obj, name=trait_value)
        trait_value_obj.save()
        print(f"Added new trait value {trait_value_obj}.")
    else:
        trait_value_obj = trait_value_obj[0]
        #  print(f"Existing trait value {trait_value_obj}.")
    return trait_value_obj

def get_trait_objs(project, trait_json):
    """Create or retrieve trait type/value objects.
    """
    trait_type = trait_json[constants.TRAIT_TYPE_KEY]
    trait_type_obj = get_trait_type_obj(project, trait_type)
    trait_value_obj = get_trait_value_obj(
            trait_type_obj, trait_json[constants.TRAIT_VALUE_KEY])
    return trait_type_obj, trait_value_obj

def get_image_url(image_url):
    """Return IPFS URL if IPFS hash else image_url.
    """
    return (f"{IPFS_URL_PREFIX}/{getIPFSHash(image_url)}" 
            if image_url.startswith("ipfs")
            else image_url)

def get_token_obj(project, number, token_json=None):
    """Create or retrieve token object with project and number.
    """
    token_obj = Token.objects.filter(
            project=project, number=number)
    if not token_obj.exists():
        token_obj = Token(project=project, number=number,
                image_url=get_image_url(token_json["image"]))
        token_obj.save()
        for trait in token_json[constants.ATTRIBUTES_KEY]:
            token_obj.traits.add(get_trait_objs(
                project, trait)[1])
        print(f"Added new token {token_obj}.")
    else:
        token_obj = token_obj[0]
    return token_obj

def get_token_name_parts(token_name):
    """Return token type/number from name.
    """
    name_parts = token_name.split("#")
    return name_parts[0].strip(), name_parts[1]

def get_token_type_obj(project, token_type):
    """Create or retrieve token type object.
    """
    token_type_obj = TokenType.objects.filter(
            project=project, name=token_type)
    if not token_type_obj.exists():
        token_type_obj = TokenType(project=project,
                name=token_type)
        token_type_obj.save()
        print(f"Added new token type {token_type_obj}.")
    else:
        token_type_obj = token_type_obj[0]
    return token_type_obj

def get_token_obj_os(project, os_asset):
    """Create or retrieve token object with OS asset JSON.
    """
    token_type, number = get_token_name_parts(os_asset["name"])
    token_type_obj = get_token_type_obj(project, token_type)

    token_obj = Token.objects.filter(
            project=project, 
            token_type=token_type_obj, 
            number=number)
    if not token_obj.exists():
        token_obj = Token(
                project=project,
                token_type=token_type_obj, 
                number=number,
                os_url=os_asset["permalink"],
                image_url=get_image_url(os_asset["image_url"]))
        token_obj.save()
        for trait in os_asset["traits"]:
            token_obj.traits.add(get_trait_objs(
                project, trait)[1])
        print(f"Added new token {token_obj}.")
    else:
        token_obj = token_obj[0]
    return token_obj
