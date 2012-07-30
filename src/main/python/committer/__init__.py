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


VERSION                          = '${version}'

OK_RETURN_CODE                   = 0

SHOW_USAGE_ERROR_CODE            = 1

NO_REPOSITORY_ERROR_CODE         = 100
TOO_MANY_REPOSITORIES_ERROR_CODE = 101
NOT_EXECUTABLE_ERROR_CODE        = 102


class CommitterException (Exception):
    def __init__ (self, message, error_code):
        self.message    = message
        self.error_code = error_code


def _error (message):
    """
        writes message to stderr.
    """

    sys.stderr.write(message + '\n')


def _detect_repository ():
    detected_repositories = repositories.detect()
    
    for repository in detected_repositories:
        sys.stdout.write('Detected %s\n' % repository.NAME)
        
    if len(detected_repositories) == 0:
        raise CommitterException('No repository detected.',
                                 NO_REPOSITORY_ERROR_CODE)
    
    if len(detected_repositories) > 1:
        raise CommitterException('More than one repository detected.',
                                 TOO_MANY_REPOSITORIES_ERROR_CODE)
    
    return detected_repositories[0]


def _ensure_command_executable(repository):
    sys.stdout.write('Checking %s command line client "%s": '
                     % (repository.NAME, repository.COMMAND))
    
    if not repository.is_executable():
        message = 'not executable!\n' \
                + 'Please install a command line client for %s ' \
                + 'repositories, providing command "%s".' \
                % repository.NAME, repository.COMMAND
        raise CommitterException(message, NOT_EXECUTABLE_ERROR_CODE)
    
    sys.stdout.write('ok.\n')


def main (arguments):
    """
        This is the main function for committer. It should be called by the
        scripts 'commit' and 'update'. When called by 'commit' it will commit
        all files in the current directory. When called by 'update' it will
        update the repository in the current directory.
    """

    sys.stdout.write('committer version %s\n' % VERSION)

    if len(arguments) == 1 and not arguments[0].endswith('update'):
        _error('usage:\n'
               '    commit "message" [++]\n'
               '    update')
        return SHOW_USAGE_ERROR_CODE
    
    try:
        repository = _detect_repository()
        _ensure_command_executable(repository)
        
        repository.update()
        
        if len(arguments) == 3 and arguments[2] == '++':
            incrementor.increment_version()
        
        if arguments[0].endswith('commit'):
            message = arguments[1]
            repository.commit(message)
            
    except CommitterException as committer_exception:
        _error(committer_exception)
        return committer_exception.error_code

    return OK_RETURN_CODE
