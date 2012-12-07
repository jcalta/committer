import unittest
import subprocess

from mockito import when, verify, unstub, any as any_value

from committer.vcsclients.util import VcsClient

import committer

class VcsClientTests (unittest.TestCase):
    def setUp(self):
        self.vcs_client = VcsClient()
        
    def tearDown(self):
        unstub()
        
    def test_should_call_command_in_subprocess (self):
        when(committer.vcsclients.util).call(any_value()).thenReturn(None)
        
        self.vcs_client.execute_command('command')
        
        verify(committer.vcsclients.util).call(['command'])

    def test_should_call_command_using_given_arguments (self):
        when(committer.vcsclients.util).call(any_value()).thenReturn(None)

        self.vcs_client.execute_command('command', '1', '2', '3')
        
        verify(committer.vcsclients.util).call(['command', '1', '2', '3'])

    def test_should_return_true_when_command_is_executable (self):
        when(committer.vcsclients.util).check_call(any_value()).thenReturn(None)
        
        actual_result = self.vcs_client.check_if_is_executable('command', '--version', '--quiet')
        
        self.assertTrue(actual_result)
        verify(committer.vcsclients.util).check_call(['command', '--version', '--quiet'])

    def test_should_return_false_when_command_is_not_executable (self):
        when(committer.vcsclients.util).check_call(any_value()).thenRaise(subprocess.CalledProcessError(127, 'command'))
        
        actual_result = self.vcs_client.check_if_is_executable('command', '--version', '--quiet')
        
        self.assertFalse(actual_result)
        verify(committer.vcsclients.util).check_call(['command', '--version', '--quiet'])

    def test_should_return_false_when_trying_to_execute_command_fails (self):
        when(committer.vcsclients.util).check_call(any_value()).thenRaise(OSError())
        
        actual_result = self.vcs_client.check_if_is_executable('command', '--version', '--quiet')
        
        self.assertFalse(actual_result)
        verify(committer.vcsclients.util).check_call(['command', '--version', '--quiet'])

    def test_should_raise_eception_when_during_check_something_unexpected_happens (self):
        when(committer.vcsclients.util).check_call(any_value()).thenRaise(Exception('Not executable'))
        
        self.assertRaises(Exception, self.vcs_client.check_if_is_executable, (['command', '--version', '--quiet']))
