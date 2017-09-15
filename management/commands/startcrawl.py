from importlib import import_module
from management.base import BaseCommand


class Command(BaseCommand):
    help = "start a spider base"

    def add_arguments(self, parser):
        parser.add_argument("spider", type=str, help="Spider name")

    def handle(self, *args, **options):

        spider_name = options['spider']
        try:
            module = import_module("spider.%s" % spider_name)
            spider = getattr(module, spider_name.lower())
            self.stdout.write("开始爬虫")
            s = spider()
            s.run()
            print(s.result.__len__())
            self.stdout.write("结束爬虫")
        except Exception as e:
            self.stderr.write(str(e))
