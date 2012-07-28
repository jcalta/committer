#   utility functions for repository wrappers module for committer
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
    Subversion wrapper module.
"""

__author__ = 'Michael Gruber'

from subprocess import CalledProcessError, call, check_call


def execute_command (command, *args):
    """
        executes command using the given arguments.
    """
    arguments = [command] + list(args)
    call(arguments)


def check_if_is_executable (*command_and_arguments):
    """
        returns True if the given  is executable, otherwise False. 
    """
    
    try:
        check_call(list(command_and_arguments))
    except CalledProcessError:
        return False
    
    return True
