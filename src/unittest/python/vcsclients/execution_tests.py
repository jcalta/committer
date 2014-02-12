#   committer
#   Copyright 2012-2014 Michael Gruber
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

import subprocess

from mock import Mock
from fluentmock import ANY_ARGUMENTS, NEVER, UnitTests, when, verify

from committer import execution

from committer.execution import check_if_is_executable, execute_command


class ExecuteCommandTests(UnitTests):

    def set_up(self):
        when(execution.LOGGER).info(ANY_ARGUMENTS).then_return(None)
        when(execution.LOGGER).error(ANY_ARGUMENTS).then_return(None)

        process_mock = Mock()
        process_mock.returncode = 0
        self.process_mock = process_mock

    def test_should_call_command_in_subprocess(self):
        when(self.process_mock).communicate().then_return(('stdout', 'stderr'))
        when(execution).Popen(ANY_ARGUMENTS).then_return(self.process_mock)

        execute_command('command')

        verify(execution).Popen(['command'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        verify(self.process_mock).communicate()

    def test_should_call_command_using_given_arguments(self):
        when(self.process_mock).communicate().then_return(('stdout', 'stderr'))
        when(execution).Popen(ANY_ARGUMENTS).then_return(self.process_mock)

        execute_command('command', '1', '2', '3')

        verify(execution).Popen(['command', '1', '2', '3'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        verify(self.process_mock).communicate()

    def test_should_return_stdout_and_stderr_and_returncode_when_executing_command(self):
        stdout = 'stdout'
        stderr = 'stderr'
        when(self.process_mock).communicate().then_return((stdout, stderr))
        when(execution).Popen(ANY_ARGUMENTS).then_return(self.process_mock)

        actual = execute_command('command', '1', '2', '3')

        self.assertEqual(stdout, actual['stdout'])
        self.assertEqual(stderr, actual['stderr'])
        self.assertEqual(0, actual['returncode'])

    def test_should_log_stdout_when_stdout_is_not_empty_string(self):
        stdout = 'stdout'
        stderr = 'stderr'
        when(self.process_mock).communicate().then_return((stdout, stderr))
        when(execution).Popen(ANY_ARGUMENTS).then_return(self.process_mock)

        execute_command('command', '1', '2', '3')

        verify(execution.LOGGER).info(stdout)

    def test_should_not_log_stdout_when_stdout_is_empty_string(self):
        stdout = ''
        stderr = 'stderr'
        when(self.process_mock).communicate().then_return((stdout, stderr))
        when(execution).Popen(ANY_ARGUMENTS).then_return(self.process_mock)

        execute_command('command', '1', '2', '3')

        verify(execution.LOGGER, NEVER).info(stdout)

    def test_should_log_stderr_when_stderr_is_not_empty_string(self):
        stdout = 'stdout'
        stderr = 'stderr'
        when(self.process_mock).communicate().then_return((stdout, stderr))
        when(execution).Popen(ANY_ARGUMENTS).then_return(self.process_mock)

        execute_command('command', '1', '2', '3')

        verify(execution.LOGGER).error(stderr)

    def test_should_not_log_stderr_when_stderr_is_empty_string(self):

        stdout = 'stdout'
        stderr = ''
        when(self.process_mock).communicate().then_return((stdout, stderr))
        when(execution).Popen(ANY_ARGUMENTS).then_return(self.process_mock)

        execute_command('command', '1', '2', '3')

        verify(execution.LOGGER, NEVER).error(stderr)

    def test_should_exit_when_execution_of_command_failed(self):

        stdout = 'stdout'
        stderr = ''
        self.process_mock.returncode = 123
        when(self.process_mock).communicate().then_return((stdout, stderr))
        when(execution).Popen(ANY_ARGUMENTS).then_return(self.process_mock)
        when(execution).exit(ANY_ARGUMENTS).then_return(None)

        execute_command('command', '1', '2', '3')

        verify(execution).exit(1)

    def test_should_catch_os_error_and_exit_when_popen_raises_exception(self):
        stdout = 'stdout'
        stderr = ''
        self.process_mock.returncode = 123
        when(self.process_mock).communicate().then_return((stdout, stderr))
        when(execution).Popen(ANY_ARGUMENTS).then_raise(OSError("[Errno 2] No such file or directory"))
        when(execution).exit(ANY_ARGUMENTS).then_return(None)

        execute_command('command', '1', '2', '3')

        verify(execution).exit(1)


class CheckIfIsExecutableTests(UnitTests):

    def test_should_return_true_when_command_is_executable(self):
        when(execution).check_call(ANY_ARGUMENTS).then_return(None)

        actual_result = check_if_is_executable('command', '--version', '--quiet')

        self.assertTrue(actual_result)
        verify(execution).check_call(['command', '--version', '--quiet'])

    def test_should_return_false_when_command_is_not_executable(self):
        when(execution).check_call(ANY_ARGUMENTS).then_raise(subprocess.CalledProcessError(127, 'command'))

        actual_result = check_if_is_executable('command', '--version', '--quiet')

        self.assertFalse(actual_result)
        verify(execution).check_call(['command', '--version', '--quiet'])

    def test_should_return_false_when_trying_to_execute_command_fails(self):
        when(execution).check_call(ANY_ARGUMENTS).then_raise(OSError())

        actual_result = check_if_is_executable('command', '--version', '--quiet')

        self.assertFalse(actual_result)
        verify(execution).check_call(['command', '--version', '--quiet'])

    def test_should_raise_exception_when_during_check_something_unexpected_happens(self):
        when(execution).check_call(ANY_ARGUMENTS).then_raise(Exception('Not executable'))

        self.assertRaises(Exception, check_if_is_executable, (['command', '--version', '--quiet']))
