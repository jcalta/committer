#   command line utility functions for committer
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
    Utility functions for command line wrappers.
"""

__author__ = 'Michael Gruber'

from subprocess import CalledProcessError, call, check_call

class AbstractVcsClient(object):
    
    def __init__(self, name, command):
        if name is None:
            raise Exception('Missing argument name when creating new vcs client')

        if command is None:
            raise Exception('Missing argument command when creating {0} vcs client'.format(name))
    
        self._command = command
        self._name = name
    
    @property
    def name(self):
        return self._name

    @property
    def command(self):
        return self._command
    
    def execute_command(self, command, *arguments):
        """
            Executes command using the given command_and_arguments.
        """
        command_and_arguments = [command] + list(arguments)
        call(command_and_arguments)
    
    
    def check_if_is_executable(self, command, *arguments):
        """
            Executes the given command with the given arguments.
            
            @return: True if the given command is executable with the given arguments,
                     False otherwise. 
        """
        try:
            command_and_arguments = [command] + list(arguments)
            check_call(command_and_arguments)
    
        except CalledProcessError:
            return False
    
        except OSError:
            return False
    
        return True

    def is_executable(self):
        raise NotImplementedError()
    
    def detect(self):
        raise NotImplementedError()
    
    def update(self):
        raise NotImplementedError()
    
    def status(self):
        raise NotImplementedError()
    
    def commit(self, message):
        raise NotImplementedError(message)
    
