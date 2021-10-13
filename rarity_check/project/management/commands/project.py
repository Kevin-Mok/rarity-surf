import project.cache as cache
import project.constants as constants
#  import project.get_obj as get_obj
from project.get_obj import get_project_obj
from project.models import Project

from django.core.management.base import BaseCommand, CommandError
from pprint import pprint

class Command(BaseCommand):
    #  def add_arguments(self, parser):
        #  parser.add_argument('num_tokens', nargs=1, type=int)

    def handle(self, *args, **options):
        # new proj
        project = Project(
                contract_address=constants.CONTRACT_ADDRESS,
                name=constants.PROJECT_NAME,
                slug=constants.PROJECT_SLUG,
                max_supply=constants.MAX_SUPPLY,
                ipfs_hash=constants.IPFS_HASH,
                api_url=constants.API_URL,
                )
        project.save()

        # modify proj
        #  project_obj = get_project_obj(
                #  constants.CONTRACT_ADDRESS,
                #  constants.PROJECT_NAME)
                #  "the-sevens")
        #  project_obj.name = constants.PROJECT_NAME
        #  project_obj.slug = constants.PROJECT_SLUG
        #  project_obj.save()

        #  project_obj.delete()
