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
    Committer provides a simplified command line interface to the
    version control systems: git, mercurial, and subverion. 
"""

__author__ = 'Michael Gruber'

import sys

from committer import errors


VERSION = '${version}'


def perform (command, arguments, usage_information):
    """
        performs the given command using the given arguments. The given
        usage_information will be passed to the perform function of the
        command module.
    """
    
    print 'committer version %s' % VERSION

    try:
        arguments = sys.argv
        
        command.perform(arguments, __doc__ + usage_information)
        
    except errors.CommitterException as committer_exception:
        sys.stderr.write(committer_exception.message)
        return committer_exception.error_code

    return 0
