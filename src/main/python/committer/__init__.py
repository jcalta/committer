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


VERSION = '${version}'


def error (message):
    """
        writes message to stderr and returns 1. The result of this function
        should be passed to the calling script.
    """

    sys.stderr.write(message + '\n')
    return 1


def main (arguments):
    """
        This is the main function for committer. It should be called by the
        scripts 'commit' and 'update'. When called by 'commit' it will commit
        all files in the current directory. When called by 'update' it will
        update the repository in the current directory.
    """

    sys.stdout.write('committer version %s\n' % VERSION)

    if len(arguments) == 1 and not arguments[0].endswith('update'):
        return error('usage:\n'
                     '    commit "message" [++]\n'
                     '    update')
    
    detected_repositories = repositories.detect()
    for repository in detected_repositories:
        sys.stdout.write('Detected %s\n' % repository.NAME)
        
    if len(detected_repositories) == 0:
        return error('No repository detected.')
    
    if len(detected_repositories) > 1:
        return error('More than one repository detected.')
    
    repository = detected_repositories[0]
    
    sys.stdout.write('Checking command line client "%s" for %s: '
                     % (repository.COMMAND, repository.NAME))
    
    if not repository.is_executable():
        return error('not executable!\n'
                     'Please install a command line client for %s '
                     'repositories, providing command "%s".' 
                     % (repository.NAME, repository.COMMAND))
    else:
        sys.stdout.write('ok.\n')
        
    repository.update()
    
    if len(arguments) == 3 and arguments[2] == '++':
        incrementor.increment_version()
    
    if arguments[0].endswith('commit'):
        message = arguments[1]
        repository.commit(message)

    return 0
