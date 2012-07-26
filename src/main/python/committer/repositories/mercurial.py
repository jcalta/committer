#   mercurial wrapper module for committer
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
    Mercurial wrapper module.
"""

__author__ = 'Michael Gruber'

from subprocess import CalledProcessError, call, check_call

from os import path


NAME = 'Mercurial'


def commit (message):
    """
        commits all files.
    """
    
    _hg('commit', '-m', message)
    _hg('push')


def detect ():
    """
        returns True if the current directory represents a mercurial repository,
        otherwise it will return False.
    """
    
    return path.isdir('.hg')


def is_executable ():
    """
        returns True if 'hg --version' is executable, otherwise False. 
    """
    try:
        arguments = ['hg', '--version']
        check_call(arguments)
    except CalledProcessError:
        return False
    
    return True


def update ():
    """
        for hg update is equal to a pull.
    """

    _hg('pull')
    _hg('update')


def _hg (*args):
    """
        executes hg using the given arguments.
    """
    
    arguments = list(args)
    arguments.insert(0, 'hg')
    call(arguments)
