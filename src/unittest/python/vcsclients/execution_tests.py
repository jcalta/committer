#   committer
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

import unittest
import subprocess

from mockito import mock, when, verify, unstub, never, any as any_value

import committer

from committer.execution import check_if_is_executable, execute_command


class ExecutionTests(unittest.TestCase):

    def tearDown(self):
        unstub()

    def test_should_call_command_in_subprocess(self):
        process_mock = mock()
        process_mock.returncode = 0
        when(process_mock).communicate().thenReturn(('stdout', 'stderr'))
        when(committer.execution.LOGGER).info(any_value()).thenReturn(None)
        when(committer.execution.LOGGER).error(any_value()).thenReturn(None)
        when(committer.execution).Popen(any_value(), stdout=any_value(), stderr=any_value(), stdin=any_value()).thenReturn(process_mock)

        execute_command('command')

        verify(committer.execution).Popen(['command'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        verify(process_mock).communicate()

    def test_should_call_command_using_given_arguments(self):
        process_mock = mock()
        process_mock.returncode = 0
        when(process_mock).communicate().thenReturn(('stdout', 'stderr'))
        when(committer.execution.LOGGER).info(any_value()).thenReturn(None)
        when(committer.execution.LOGGER).error(any_value()).thenReturn(None)
        when(committer.execution).Popen(any_value(), stdout=any_value(), stderr=any_value(), stdin=any_value()).thenReturn(process_mock)

        execute_command('command', '1', '2', '3')

        verify(committer.execution).Popen(['command', '1', '2', '3'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        verify(process_mock).communicate()

    def test_should_return_stdout_and_stderr_and_returncode_when_executing_command(self):
        stdout = 'stdout'
        stderr = 'stderr'
        process_mock = mock()
        process_mock.returncode = 0
        when(process_mock).communicate().thenReturn((stdout, stderr))
        when(committer.execution.LOGGER).info(any_value()).thenReturn(None)
        when(committer.execution.LOGGER).error(any_value()).thenReturn(None)
        when(committer.execution).Popen(any_value(), stdout=any_value(), stderr=any_value(), stdin=any_value()).thenReturn(process_mock)

        actual = execute_command('command', '1', '2', '3')

        self.assertEqual(stdout, actual['stdout'])
        self.assertEqual(stderr, actual['stderr'])
        self.assertEqual(0, actual['returncode'])

    def test_should_print_stdout_when_stdout_is_not_empty_string(self):
        stdout = 'stdout'
        stderr = 'stderr'
        process_mock = mock()
        process_mock.returncode = 0
        when(process_mock).communicate().thenReturn((stdout, stderr))
        when(committer.execution.LOGGER).info(any_value()).thenReturn(None)
        when(committer.execution.LOGGER).error(any_value()).thenReturn(None)
        when(committer.execution).Popen(any_value(), stdout=any_value(), stderr=any_value(), stdin=any_value()).thenReturn(process_mock)

        execute_command('command', '1', '2', '3')

        verify(committer.execution.LOGGER).info(stdout)

    def test_should_not_print_stdout_when_stdout_is_empty_string(self):
        stdout = ''
        stderr = 'stderr'
        process_mock = mock()
        process_mock.returncode = 0
        when(process_mock).communicate().thenReturn((stdout, stderr))
        when(committer.execution.LOGGER).info(any_value()).thenReturn(None)
        when(committer.execution.LOGGER).error(any_value()).thenReturn(None)
        when(committer.execution).Popen(any_value(), stdout=any_value(), stderr=any_value(), stdin=any_value()).thenReturn(process_mock)

        execute_command('command', '1', '2', '3')

        verify(committer.execution, never).print_text(stdout)

    def test_should_print_stderr_when_stderr_is_not_empty_string(self):
        stdout = 'stdout'
        stderr = 'stderr'
        process_mock = mock()
        process_mock.returncode = 0
        when(process_mock).communicate().thenReturn((stdout, stderr))
        when(committer.execution.LOGGER).info(any_value()).thenReturn(None)
        when(committer.execution.LOGGER).error(any_value()).thenReturn(None)
        when(committer.execution).Popen(any_value(), stdout=any_value(), stderr=any_value(), stdin=any_value()).thenReturn(process_mock)

        execute_command('command', '1', '2', '3')

        verify(committer.execution.LOGGER).error(stderr)

    def test_should_not_print_stderr_when_stderr_is_empty_string(self):

        stdout = 'stdout'
        stderr = ''
        process_mock = mock()
        process_mock.returncode = 0
        when(process_mock).communicate().thenReturn((stdout, stderr))
        when(committer.execution.LOGGER).info(any_value()).thenReturn(None)
        when(committer.execution.LOGGER).error(any_value()).thenReturn(None)
        when(committer.execution).Popen(any_value(), stdout=any_value(), stderr=any_value(), stdin=any_value()).thenReturn(process_mock)

        execute_command('command', '1', '2', '3')

        verify(committer.execution, never).print_error(stderr)

    def test_should_exit_when_execution_of_command_failed(self):

        stdout = 'stdout'
        stderr = ''
        process_mock = mock()
        process_mock.returncode = 123
        when(process_mock).communicate().thenReturn((stdout, stderr))
        when(committer.execution.LOGGER).info(any_value()).thenReturn(None)
        when(committer.execution.LOGGER).error(any_value()).thenReturn(None)
        when(committer.execution).Popen(any_value(), stdout=any_value(), stderr=any_value(), stdin=any_value()).thenReturn(process_mock)
        when(committer.execution).exit(any_value()).thenReturn(None)

        execute_command('command', '1', '2', '3')

        verify(committer.execution).exit(1)

    def test_should_return_true_when_command_is_executable(self):
        when(committer.execution).check_call(any_value()).thenReturn(None)

        actual_result = check_if_is_executable('command', '--version', '--quiet')

        self.assertTrue(actual_result)
        verify(committer.execution).check_call(['command', '--version', '--quiet'])

    def test_should_return_false_when_command_is_not_executable(self):
        when(committer.execution).check_call(any_value()).thenRaise(subprocess.CalledProcessError(127, 'command'))

        actual_result = check_if_is_executable('command', '--version', '--quiet')

        self.assertFalse(actual_result)
        verify(committer.execution).check_call(['command', '--version', '--quiet'])

    def test_should_return_false_when_trying_to_execute_command_fails(self):
        when(committer.execution).check_call(any_value()).thenRaise(OSError())

        actual_result = check_if_is_executable('command', '--version', '--quiet')

        self.assertFalse(actual_result)
        verify(committer.execution).check_call(['command', '--version', '--quiet'])

    def test_should_raise_exception_when_during_check_something_unexpected_happens(self):
        when(committer.execution).check_call(any_value()).thenRaise(Exception('Not executable'))

        self.assertRaises(Exception, check_if_is_executable, (['command', '--version', '--quiet']))
