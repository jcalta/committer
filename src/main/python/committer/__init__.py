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

from sys import exit, stdout, stderr
from committer import errors
from committer.actions import commit
from committer.actions import status
from committer.actions import update


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


    def __call__(self, arguments):
        """
            performs the given command using the given arguments.
        """
        if len(arguments) > 1:
            if arguments[1] == '--version':
                stdout.write('{0} version {1}\n'.format(__name__, __version__))
                return exit(0)

            if arguments[1] in ['help', '--help', '-h']:
                stdout.write(USAGE_INFORMATION)
                return exit(0)

        try:
            self.function(arguments)
            return exit(0)

        except errors.CommitterError as committer_exception:
            stderr.write(committer_exception.message)
            return exit(committer_exception.error_code)


@ScriptCommand
def commit_changes(arguments):
    commit(arguments)


@ScriptCommand
def show_status(arguments):
    status(arguments)


@ScriptCommand
def update_files(arguments):
    update(arguments)
