from management.base import BaseCommand
from timeit import timeit


class Command(BaseCommand):
    help = "start a spider base"

    def add_arguments(self, parser):
        parser.add_argument("spider", type=str, help="Spider name")

    def handle(self, *args, **options):

        spider_name = options['spider']
        try:
            self.stdout.write("开始爬虫")
            spider_time = timeit("engine('{}')".format(spider_name.lower()), setup="from base.engine import engine",
                                 number=1)
            self.stdout.write("结束爬虫 耗时{}".format(str(spider_time)))
        except Exception as e:
            self.stderr.write(str(e))
