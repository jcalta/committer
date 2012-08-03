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

from committer import repositories, incrementor


VERSION                     = '${version}'

OK_RETURN_CODE              = 0

NO_ARGUMENTS_ERROR          = ('usage:\n'
                               '    commit "message" [++]\n'
                               '    update', 1)

NO_REPOSITORY_ERROR         = ('No repository detected.', 100)
TOO_MANY_REPOSITORIES_ERROR = ('More than one repository detected.', 101)
NOT_EXECUTABLE_ERROR        = ('Command line client not executable.', 102)

class CommitterException (Exception):
    """
        to be raised when an error occurred, which should stop the default
        program flow.
    """
    
    def __init__ (self, error_tuple):
        """
            will set the given properties.
        """
        
        super(CommitterException, self).__init__()
        self.message    = error_tuple[0]
        self.error_code = error_tuple[1]


def _detect_repository ():
    """
        returns the detected repository. Will raise an CommitterException when
        no or more than one repository is detected.
    """
    
    detected_repositories = repositories.detect()
    
    for repository in detected_repositories:
        sys.stdout.write('Detected %s\n' % repository.NAME)
        
    if len(detected_repositories) == 0:
        raise CommitterException(NO_REPOSITORY_ERROR)
    
    if len(detected_repositories) > 1:
        raise CommitterException(TOO_MANY_REPOSITORIES_ERROR)
    
    return detected_repositories[0]


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
        raise CommitterException(NOT_EXECUTABLE_ERROR)
    
    sys.stdout.write('ok.\n')


def _committer(arguments):
    """
        1. detect what kind of repository the current directory is.
        2. ensure the command line client for the repository is executable.
        3. update the repository.
        4. optionally execute an incrementor.
        5. commit all modified files to the repository.
    """

    repository = _detect_repository()
    _ensure_command_executable(repository)
    
    repository.update()
    
    if len(arguments) == 3 and arguments[2] == '++':
        incrementor.increment_version()
        
    if arguments[0].endswith('commit'):
        message = arguments[1]
        repository.commit(message)


def main (arguments):
    """
        This is the main function for committer. It should be called by the
        scripts 'commit' and 'update'. When called by 'commit' it will commit
        all files in the current directory. When called by 'update' it will
        update the repository in the current directory.
    """

    sys.stdout.write('committer version %s\n' % VERSION)

    try:
        if len(arguments) == 1 and not arguments[0].endswith('update'):
            raise CommitterException(NO_ARGUMENTS_ERROR)
        
        _committer(arguments)
        
    except CommitterException as committer_exception:
        sys.stderr.write(committer_exception.message + '\n')
        return committer_exception.error_code

    return OK_RETURN_CODE
