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

from committer import repositories, handler


VERSION = '${version}'


def error (message):
    """
        writes message to stderr and returns 1. The result of this function
        should be passed to the calling script.
    """
    
    sys.stderr.write(message)
    return 1

def main (arguments):
    """
        will exit with 1 when no arguments are given.
        will use first argument as commit message.
        will increment if second argument is ++
    """
    
    sys.stdout.write('committer version %s\n' % VERSION)
    
    if len(arguments) == 1:
        return error('usage:\n'
                     '    commit "message" [++]\n') 
    
    detected_repositories = repositories.detect()
    if len(detected_repositories) == 0:
        return error('Could not detect any repository.\n')
    
    if len(detected_repositories) > 1:
        return error('More than one repository detected.\n')
    
    repository = detected_repositories[0]
    
    message = arguments[1]
    if len(arguments) == 3 and arguments[2] == '++':
        return handler.commit(repository, message, increment=True)
        
    return handler.commit(repository, message)
