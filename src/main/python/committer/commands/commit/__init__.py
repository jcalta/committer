#   committer commit command
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
"""

__author__ = 'Michael Gruber'

from committer import errors, repositories
from committer.commands.commit import incrementor


def perform(arguments, usage_information):
    """
        1. detect what kind of repository the current directory is.
        2. update the repository.
        3. optionally execute an incrementor.
        4. commit all modified files to the repository.
    """

    if len(arguments) == 1:
        raise errors.CommitterException(usage_information, 1)
        
    repository = repositories.discover_working_repository()
    repository.update()
    
    if len(arguments) == 3 and arguments[2] == '++':
        incrementor.increment_version()
        
    message = arguments[1]
    repository.commit(message)
