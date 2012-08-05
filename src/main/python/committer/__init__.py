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
    Committer main module.
"""

__author__ = 'Michael Gruber'

import sys

from committer import repositories, incrementor, errors


VERSION = '${version}'


def _detect_repository ():
    """
        returns the detected repository. Will raise an CommitterException when
        no or more than one repository is detected.
    """
    
    detected_repositories = repositories.detect()
    
    for repository in detected_repositories:
        sys.stdout.write('Detected %s repository.\n' % repository.NAME)
        
    if len(detected_repositories) == 0:
        raise errors.NoRepositoryDetectedException()
    
    if len(detected_repositories) > 1:
        raise errors.TooManyRepositoriesException()
    
    repository = detected_repositories[0]
    return _ensure_command_executable(repository)


def _ensure_command_executable(repository):
    """
        ensures that the command line client for the given repository is
        executable. Will Raise an CommiterException when the command line
        client is not executable.
    """
    
    sys.stdout.write('Checking %s command line client "%s": '
                     % (repository.NAME, repository.COMMAND))
    
    if not repository.is_executable():
        sys.stdout.write('failed!\n')
        raise errors.NotExecutableException(repository)
    
    sys.stdout.write('ok.\n')
    
    return repository


def commit(arguments):
    """
        1. detect what kind of repository the current directory is.
        2. update the repository.
        3. optionally execute an incrementor.
        4. commit all modified files to the repository.
    """

    repository = _detect_repository()
    repository.update()
    
    if len(arguments) == 3 and arguments[2] == '++':
        incrementor.increment_version()
        
    message = arguments[1]
    repository.commit(message)


def update():
    """
        Updates the repository in the current directory.
    """

    repository = _detect_repository()
    repository.update()
