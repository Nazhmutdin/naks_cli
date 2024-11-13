from click import Group
from collections import OrderedDict


__all__ = [
    "welder_commands",
    "welder_certification_commands",
    "ndt_commands",
    "parse_commands",
    "AuthorizateCommand"
]


class OrderedGroup(Group):
    def __init__(self, name=None, commands=None, **attrs):
        super(OrderedGroup, self).__init__(name, commands, **attrs)
        self.commands = commands or OrderedDict()

    def list_commands(self, ctx):
        return self.commands
