from argparse import ArgumentParser
import os , sys


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


# class OutputWrapper(object):
#     @property
#     def style_func(self):
#         return self._style_func
#
#     @style_func.setter
#     def style_func(self, style_func):
#         if style_func and self.isatty():
#             self._style_func = style_func
#         else:
#             self._style_func = lambda x: x
#
#     def __init__(self, out, style_func=None, ending='\n'):
#         self._out = out
#         self.style_func = None
#         self.ending = ending
#
#     def __getattr__(self, name):
#         return getattr(self._out, name)
#
#     def isatty(self):
#         return hasattr(self._out, 'isatty') and self._out.isatty()
#
#     def write(self, msg, style_func=None, ending=None):
#         ending = self.ending if ending is None else ending
#         if ending and not msg.endswith(ending):
#             msg += ending
#         style_func = style_func or self.style_func
#         self._out.write(style_func(msg))


class BaseCommand(object):
    help = ''
    _called_from_command_line = False

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        raise NotImplementedError('subclasses of BaseCommand must provide a handle() method')

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
        except Exception as e:
            raise ValueError(e)
        return output

    def run(self, argv):
        self._called_from_command_line = True
        parser = self.create_parser(argv[0], argv[1])
        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)
        args = cmd_options.pop('args', ())
        try:
            self.execute(*args, **cmd_options)
        except Exception as e:
            raise ValueError(e)
