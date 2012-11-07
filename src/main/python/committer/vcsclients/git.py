#   git client for committer
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
    Git command line client wrapper module.
"""

__author__ = 'Michael Gruber'

from os import path

from committer.vcsclients.util import check_if_is_executable, execute_command


COMMAND = 'git'
NAME = 'Git'


def commit (message):
    """
        commits all files by calling: git commit -a -m "message"
    """
    
    _git('commit', '-a', '-m', message)
    _git('push')


def detect ():
    """
        Checks if the .git directory exists.
        
        @return: True if the current directory represents a git repository,
                 otherwise False.
    """
    
    return path.isdir('.git')


def is_executable ():
    """
        Checks if "git --version" is executable
         
        @return: True git command line client executable, otherwise False. 
    """
    
    return check_if_is_executable(COMMAND, '--version')


def status ():
    """
        Shows changes in current directory using "git status".
    """

    _git('status', '-sb')


def update ():
    """
        Updates files by executing "git pull".
    """

    _git('pull')


def _git (*arguments):
    """
        Executes git using the given arguments.
    """
    
    execute_command(COMMAND, *arguments)
