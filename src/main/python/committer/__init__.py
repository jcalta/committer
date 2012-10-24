#   committer
#   Copyright 2012 Michael Gruber
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


_USAGE_INFORMATION = """
usage:
    commit "message" [++]    commits all changes
    st                       shows all changes
    update                   updates the current directory
"""

def perform (command, arguments):
    """
        performs the given command using the given arguments.
    """

    stdout.write('committer version %s\n' % __version__)

    if len(arguments) > 1 and arguments[1] == '--version':
        return exit(0)

    if len(arguments) > 1 and arguments[1] == 'help':
        stdout.write(_USAGE_INFORMATION)
        return exit(0)

    try:
        command.perform(arguments)
        return exit(0)

    except errors.CommitterException as committer_exception:
        stderr.write(committer_exception.message)
        return exit(committer_exception.error_code)
