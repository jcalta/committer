import unittest
import subprocess

from mockito import mock, when, verify, unstub, any as any_value

import committer

from committer.vcsclients import AbstractVcsClient


class AbstractVcsClientTests (unittest.TestCase):
    def setUp(self):
        self.vcs_client = AbstractVcsClient('Name', 'command')

    def tearDown(self):
        unstub()

    def test_should_raise_exception_when_argument_name_not_given(self):
        self.assertRaises(Exception, AbstractVcsClient, None, 'command')

    def test_should_raise_exception_when_argument_command_not_given(self):
        self.assertRaises(Exception, AbstractVcsClient, 'Name', None)

    def test_should_have_property_name(self):
        self.assertEqual('Name', self.vcs_client.name)

    def test_should_have_property_command(self):
        self.assertEqual('command', self.vcs_client.command)

    def test_should_call_command_in_subprocess (self):
        process_mock = mock()
        when(committer.vcsclients).Popen(any_value()).thenReturn(process_mock)

        self.vcs_client.execute_command('command')

        verify(committer.vcsclients).Popen(['command'])
        verify(process_mock).communicate()

    def test_should_call_command_using_given_arguments (self):
        process_mock = mock()
        when(committer.vcsclients).Popen(any_value()).thenReturn(process_mock)

        self.vcs_client.execute_command('command', '1', '2', '3')

        verify(committer.vcsclients).Popen(['command', '1', '2', '3'])
        verify(process_mock).communicate()

    def test_should_return_true_when_command_is_executable (self):
        when(committer.vcsclients).check_call(any_value()).thenReturn(None)

        actual_result = self.vcs_client.check_if_is_executable('command', '--version', '--quiet')

        self.assertTrue(actual_result)
        verify(committer.vcsclients).check_call(['command', '--version', '--quiet'])

    def test_should_return_false_when_command_is_not_executable (self):
        when(committer.vcsclients).check_call(any_value()).thenRaise(subprocess.CalledProcessError(127, 'command'))

        actual_result = self.vcs_client.check_if_is_executable('command', '--version', '--quiet')

        self.assertFalse(actual_result)
        verify(committer.vcsclients).check_call(['command', '--version', '--quiet'])

    def test_should_return_false_when_trying_to_execute_command_fails (self):
        when(committer.vcsclients).check_call(any_value()).thenRaise(OSError())

        actual_result = self.vcs_client.check_if_is_executable('command', '--version', '--quiet')

        self.assertFalse(actual_result)
        verify(committer.vcsclients).check_call(['command', '--version', '--quiet'])

    def test_should_raise_exception_when_during_check_something_unexpected_happens (self):
        when(committer.vcsclients).check_call(any_value()).thenRaise(Exception('Not executable'))

        self.assertRaises(Exception, self.vcs_client.check_if_is_executable, (['command', '--version', '--quiet']))

    def test_should_raise_not_implemented_error_when_trying_to_check_if_is_executable(self):
        self.assertRaises(NotImplementedError, self.vcs_client.is_executable)

    def test_should_raise_not_implemented_error_when_trying_to_detect(self):
        self.assertRaises(NotImplementedError, self.vcs_client.detect)

    def test_should_raise_not_implemented_error_when_trying_to_update(self):
        self.assertRaises(NotImplementedError, self.vcs_client.update)

    def test_should_raise_not_implemented_error_when_trying_to_get_status(self):
        self.assertRaises(NotImplementedError, self.vcs_client.status)

    def test_should_raise_not_implemented_error_when_trying_to_commit(self):
        self.assertRaises(NotImplementedError, self.vcs_client.commit, 'message')
