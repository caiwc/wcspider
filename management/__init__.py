from importlib import import_module
import os, sys
import pkgutil

from management.base import CommandParser, BaseCommand
from management import commands


def get_all_commands():
    command_list = [name for _, name, ispkg in pkgutil.iter_modules(commands.__path__, commands.__name__ + ".") if
                    not ispkg and not name.startswith('_')]
    return command_list


def get_command(subcommand):
    command_list = get_all_commands()
    for command in command_list:
        if subcommand == command.split(".")[-1]:
            return import_module(command)
    return None


class Management(object):
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        self.settings_exception = None

    def help_text(self):
        command_lsit = get_all_commands()
        text = [command.split(".")[-1] for command in command_lsit]
        text.insert(0,"有如下命令:")
        return "\n".join(text)

    def fetch_command(self, subcommand):
        task = get_command(subcommand)
        if not task:
            raise ValueError

        if isinstance(task, BaseCommand):
            klass = task
        else:
            klass = task.Command()
        return klass

    def execute(self):
        try:
            subcommand = self.argv[1]
        except:
            subcommand = "help"

        parser = CommandParser(None, usage="%(prog)s subcommand [options] [args]", add_help=False)
        parser.add_argument('args', nargs='*')  # set all args
        options, args = parser.parse_known_args(self.argv[2:])

        if subcommand == "help":
            if len(options.args) < 1:
                sys.stdout.write(self.help_text() + '\n')
            else:
                self.fetch_command(options.args[0]).print_help(self.prog_name, options.args[0])
        else:
            self.fetch_command(subcommand).run(self.argv)


def execute_command(argv=None):
    m = Management(argv)
    m.execute()
