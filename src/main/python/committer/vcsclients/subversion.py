#   subversion client for committer
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
    Subversion command line client wrapper module.
"""

__author__ = 'Michael Gruber'

from os import path

from committer.vcsclients.util import check_if_is_executable, execute_command


COMMAND = 'svn'
NAME = 'Subversion'

def commit (message):
    """
        Commits all files by calling: svn commit -m "message"
    """
    
    _svn('commit', '-m', message)


def detect ():
    """
        Checks if the .svn directory exists.
        
        @return: True if the current directory represents a subversion repository,
                 otherwise False.
    """
    
    return path.isdir('.svn')


def is_executable ():
    """
        Checks if "svn --version --quiet" is executable.
        
        @return: True if svn client is executable, otherwise False. 
    """
    
    return check_if_is_executable(COMMAND, '--version', '--quiet')


def status ():
    """
        Shows changes in the current directory using "svn status".
    """

    _svn('status')


def update ():
    """
        Updates files by executing "svn pull" and "svn update".
    """

    _svn('update')


def _svn (*arguments):
    """
        Executes svn using the given arguments.
    """
    
    execute_command(COMMAND, *arguments)
