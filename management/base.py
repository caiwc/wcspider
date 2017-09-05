from argparse import ArgumentParser
import os, sys


class CommandParser(ArgumentParser):
    def __init__(self, cmd, **kwargs):
        self.cmd = cmd
        super(CommandParser, self).__init__(**kwargs)

    def parse_args(self, args=None, namespace=None):

        return super(CommandParser, self).parse_args(args, namespace)

    def error(self, message):
        if self.cmd._called_from_command_line:
            super(CommandParser, self).error(message)
        else:
            raise Exception("Error: %s" % message)


class OutputWrapper(object):
    def __init__(self, out, ending='\n'):
        self._out = out
        self.style_func = None
        self.ending = ending

    def write(self, msg, ending=None):
        ending = self.ending if ending is None else ending
        if ending and not msg.endswith(ending):
            msg += ending
        self._out.write(msg)


class BaseCommand(object):
    help = ''
    _called_from_command_line = False

    def __init__(self):
        self.stdout = OutputWrapper(sys.stdout)
        self.stderr = OutputWrapper(sys.stderr)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        raise NotImplementedError('subclasses of BaseCommand must provide a handle() method')

    def print_help(self, prog_name, subcommand):
        parser = self.create_parser(prog_name, subcommand)
        parser.print_help()

    def create_parser(self, prog_name, subcommand):
        parser = CommandParser(
            self, prog="%s %s" % (os.path.basename(prog_name), subcommand),
            description=self.help or None,
        )
        self.add_arguments(parser)
        return parser

    def execute(self, *args, **options):
        try:
            output = self.handle(*args, **options)
            return output
        except Exception as e:
            self.stderr.write(str(e))

    def run(self, argv):
        self._called_from_command_line = True
        parser = self.create_parser(argv[0], argv[1])
        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)
        args = cmd_options.pop('args', ())
        try:
            self.execute(*args, **cmd_options)
        except Exception as e:
            self.stderr.write(str(e))
