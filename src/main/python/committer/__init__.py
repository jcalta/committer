#   committer
#   Copyright 2012-2013 Michael Gruber
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
    committer provides a unified and simplified command line interface to
    the version control systems: git, mercurial, and subverion.
"""

__author__ = 'Michael Gruber'
__version__ = '${version}'

from sys import exit

from committer import errors
from committer.actions import commit, status, update
from committer.terminal import print_error, print_text

USAGE_INFORMATION = """
usage:
    ci "message"     commits all changes
    st               shows all changes
    up               updates the current directory
"""


class ScriptCommand(object):
    """
        Decorator for functions which are called from scripts.
    """
    def __init__(self, function):
        self.function = function

    def _handle_version_argument(self, arguments):
        """
            Shows the version and exits the program, if arguments contains --version.
        """
        if '--version' in arguments:
            print_text('{0} version {1}\n'.format(__name__, __version__))
            return exit(0)

    def _handle_help_argument(self, arguments):
        """
            Shows the usage information and exits the program, if arguments contains
            help, --help, or -h.
        """
        for help_option in ['help', '--help', '-h']:
            if help_option in arguments:
                print_text(USAGE_INFORMATION)
                return exit(0)

    def _filter_unused_argument_dash_m(self, arguments):
        """
            Returns a list which equals the given one, but removes the string '-m' from it.
        """
        return [argument for argument in arguments if argument != '-m']

    def __call__(self, arguments):
        """
            performs the given command using the given arguments.
        """
        filtered_arguments = self._filter_unused_argument_dash_m(arguments)

        if len(filtered_arguments) > 1:
            self._handle_version_argument(filtered_arguments)
            self._handle_help_argument(filtered_arguments)

        try:
            self.function(filtered_arguments)
            return exit(0)

        except errors.CommitterError as committer_exception:
            print_error(committer_exception.message)
            return exit(committer_exception.error_code)

        except KeyboardInterrupt:
            print_error('Interrupted by user.\n')
            return exit(-1)


@ScriptCommand
def commit_changes(arguments):
    commit(arguments)


@ScriptCommand
def show_status(arguments):
    status(arguments)


@ScriptCommand
def update_files(arguments):
    update(arguments)
