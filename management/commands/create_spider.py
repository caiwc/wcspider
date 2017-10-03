from settings import base_path
from management.script import script
from management.base import BaseCommand


class Command(BaseCommand):
    help = "create a spider by name"

    def add_arguments(self, parser):
        parser.add_argument("spider_name", type=str, help="Spider name")

    def handle(self, *args, **options):
        spider_name = options['spider_name']
        with open(base_path + "/spider/" + spider_name + ".py", "w+") as f:
            f.write(script % spider_name)
            f.close()
