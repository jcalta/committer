#   git wrapper module for committer
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
    Git wrapper module.
"""

import subprocess

from os import path


NAME = 'git'


def commit (message):
    """
        commits all files.
    """
    
    _git('commit', '-a', '-m', message)


def detect ():
    """
        returns True if the current directory represents a git repository,
        otherwise it will return False.
    """
    
    return path.isdir('.git')


def pull ():
    """
        pulls from repository.
    """
    
    _git('pull')


def push ():
    """
        pushes to repository.
    """
    
    _git('push')


def _git (*args):
    """
        executes git using the given arguments.
    """
    
    arguments = list(args)
    arguments.insert(0, 'git')
    subprocess.call(arguments)


def _ensure_git_is_executable ():
    """
        checks that 'git --version' can be executed,
        will raise an exception if not.
    """
    
    arguments = ['git', '--version']
    subprocess.check_call(arguments)
