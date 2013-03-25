#   version control system clients for committer
#   Copyright 2012-2013 Michael Gruber
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
    Submodules of this module contain version control system clients which
    implement the AbstractVcsClient provided by this module.
"""

__author__ = 'Michael Gruber'

from subprocess import PIPE, CalledProcessError, Popen, check_call

from committer.terminal import print_error, print_text


class AbstractVcsClient(object):
    """
        VCS Clients need to implement this class and override commit, detect, is_executable, status, and update.
    """
    def __init__(self, name, command):
        """
            Asserts that the arguments name and command are set and will set the corresponding private properties.
        """
        if name is None:
            raise Exception('Missing argument "name" when creating new vcs client')

        if command is None:
            raise Exception('Missing argument "command" when creating {0} vcs client'.format(name))

        self._command = command
        self._name = name

    @property
    def command(self):
        """
            name of command line client.
        """
        return self._command

    @property
    def name(self):
        """
            Name of version control system.
        """
        return self._name

    def check_if_is_executable(self, command, *arguments):
        """
            Executes the given command with the given arguments.

            @return: True if the given command is executable with the given arguments,
                     False otherwise.
        """
        try:
            command_with_arguments = [command] + list(arguments)
            check_call(command_with_arguments)

        except CalledProcessError:
            return False

        except OSError:
            return False

        return True

    def execute_command(self, command, *arguments):
        """
            Executes command using the given arguments.
        """
        command_with_arguments = [command] + list(arguments)
        process = Popen(command_with_arguments, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        stdout, stderr = process.communicate()

        if stdout != '':
            print_text(stdout)

        if stderr != '':
            print_error(stderr)

        returncode = process.returncode

        return {'stdout': stdout, 'stderr': stderr, 'returncode': returncode}

    def is_executable(self):
        """
            Override this method with a check if the vcs command line client is executable.

            should return: True if client is executable,
                           False otherwise.

            @return: raises NotImplementedError
        """
        raise NotImplementedError()

    def detect(self):
        """
            Override this method with a check if the current directory represents a working directory of this client.

            should return: True if the directory is a working directory handled by this client,
                           False otherwise.

            @return: raises NotImplementedError
        """
        raise NotImplementedError()

    @property
    def everything_was_up_to_date(self):
        """
            Override this property with a check if the last update found changes.

            should return: True if no updates have been found,
                           False otherwise.

            @return: True
        """
        return True

    def update(self):
        """
            Override this method with a update function.
        """
        raise NotImplementedError()

    def status(self):
        """
            Override this method with a function which shows changes in current working directory.
        """
        raise NotImplementedError()

    def commit(self, message):
        """
            Override this method with a function which commits all files.
        """
        raise NotImplementedError('Commit method has been called with argument message="{0}" '.format(message))
