import logging
import os
import sys
from optparse import AmbiguousOptionError, BadOptionError, OptionParser


class PassThroughOptionParser(OptionParser):
    """
    An unknown option pass-through implementation of OptionParser.

    When unknown arguments are encountered, bundle with largs and try again,
    until rargs is depleted.

    sys.exit(status) will still be called if a known argument is passed
    incorrectly (e.g. missing arguments or bad argument types, etc.)
    """

    def _process_args(self, largs, rargs, values):
        while rargs:
            try:
                OptionParser._process_args(self, largs, rargs, values)
            except (BadOptionError, AmbiguousOptionError), e:
                largs.append(e.opt_str)


def get_logger(program_name=None, to_console=True, console_level=logging.DEBUG):
    if program_name is None or program_name == '__main__':
        program_name = os.path.basename(sys.argv[0])
        if program_name.endswith('.py'):
            program_name = program_name[:-3]
    my_logger = logging.getLogger(program_name)
    if to_console:
        consolehandler = logging.StreamHandler()
        consolehandler.setLevel(console_level)
        consoleformatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        consolehandler.setFormatter(consoleformatter)
        my_logger.addHandler(consolehandler)
    return my_logger


usage = "usage: %prog --settings=SETTINGS"
parser = PassThroughOptionParser(usage, add_help_option=False)
parser.add_option('--settings', dest='settings', metavar='SETTINGS', default='tendril_exercise.settings',
                  help="The Django settings module to use")
(options, args) = parser.parse_args()
if not options.settings:
    parser.error("You must specify a settings module")
add_path = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-3])
sys.path = [add_path, ] + sys.path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', options.settings)
