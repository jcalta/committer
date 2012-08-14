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

from sys import stdout, stderr

from committer import errors


VERSION = '${version}'


def perform (command, arguments, usage_information):
    """
        performs the given command using the given arguments. The given
        usage_information will be passed to the perform function of the
        command module.
    """
    
    stdout.write('committer version %s\n' % VERSION)
    return_code = 0
    
    if len(arguments) > 1 and arguments[1] == '--version':
        return exit(return_code)
    
    complete_usage_information = __doc__ + usage_information + '\n'
    
    if len(arguments) > 1 and arguments[1] == 'help':
        stdout.write(complete_usage_information)
        return exit(return_code)
    
    try:
        command.perform(arguments, complete_usage_information)
        
    except errors.CommitterException as committer_exception:
        stderr.write(committer_exception.message)
        return_code = committer_exception.error_code

    exit(return_code)
