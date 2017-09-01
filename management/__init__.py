from importlib import import_module
import os, sys
import pkgutil

from management.base import CommandParser
from management import commands


def get_command(subcommand):
    command_list = [name for _, name, ispkg in pkgutil.iter_modules(commands.__path__, commands.__name__ + ".") if
                    not ispkg and not name.startswith('_')]
    for command in command_list:
        if subcommand == command.split(".")[-1]:
            return import_module(command)
    return None


class Management(object):
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        self.settings_exception = None

    def fetch_command(self, subcommand):
        task = get_command(subcommand)
        if not task:
            raise ValueError


    def execute(self):
        try:
            subcommand = self.argv[1]
        except:
            subcommand = "help"


if __name__ == '__main__':
    xx=get_command("startcrawl")

