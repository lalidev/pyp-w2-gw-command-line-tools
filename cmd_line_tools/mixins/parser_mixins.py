import sys
import argparse

__all__ = ['SimpleCommandLineParserMixin']


class SimpleCommandLineParserMixin(object):
    ARGUMENTS_ATTR_NAME = '_arguments'

    def parse_arguments(self):
        arguments = getattr(self, self.ARGUMENTS_ATTR_NAME, {})

        for argv in sys.argv:
            if '=' in argv:
                arguments.update(dict([tuple(argv.split('='))]))

        # Equivalent:
        # self._arguments = arguments
        setattr(self, self.ARGUMENTS_ATTR_NAME, arguments)


# Can you implement an argparse version?
