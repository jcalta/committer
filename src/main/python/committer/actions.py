#   committer actions
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
    Using the "commit" command will discover the working repository in
    the current directory.

    The "status" command discovers all changes in the in the current directory.

    Using the "update" command will discover the working repository in
    the current directory.
"""

__author__ = 'Michael Gruber'

from committer.errors import WrongUsageError
from committer.vcsclients import discover_working_repository


def commit(arguments):
    """
        1. detect what kind of repository the current directory is.
        2. perform update using the vcs_client.
        3. optionally execute an incrementor.
        4. commit all modified files to the repository using the vcs client.
    """
    if len(arguments) == 1:
        raise WrongUsageError()

    vcs_client = discover_working_repository()
    vcs_client.update()

    message = arguments[1]
    vcs_client.commit(message)

def status(arguments):
    """
        Shows all changes in the current working directory.
    """
    if len(arguments) != 1:
        raise WrongUsageError()

    vcs_client = discover_working_repository()
    vcs_client.status()


def update(arguments):
    """
        Updates the repository in the current working directory.
    """
    if len(arguments) != 1:
        raise WrongUsageError()

    vcs_client = discover_working_repository()
    vcs_client.update()