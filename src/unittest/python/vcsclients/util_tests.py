import unittest
import subprocess

from mock import call, patch

from committer.vcs_clients.util import VcsClient


class ExecuteCommandTests (unittest.TestCase):
    @patch('committer.vcs_clients.util.call')        
    def test_should_call_command_in_subprocess (self, mock_call):
        vcs_client = VcsClient()
        
        vcs_client.execute_command('command')
        
        self.assertEqual(call(['command']), mock_call.call_args)

    @patch('committer.vcs_clients.util.call')        
    def test_should_call_command_using_given_arguments (self, mock_call):
        vcs_client = VcsClient()
        
        vcs_client.execute_command('command', '1', '2', '3')
        
        self.assertEqual(call(['command', '1', '2', '3']), mock_call.call_args)

        
class CheckIfIsExecutableTests (unittest.TestCase):
    @patch('committer.vcs_clients.util.check_call')        
    def test_should_return_true_when_command_is_executable (self, mock_check_call):
        vcs_client = VcsClient()

        actual_result = vcs_client.check_if_is_executable('command', '--version', '--quiet')
        
        self.assertTrue(actual_result)
        self.assertEqual(call(['command', '--version', '--quiet']), mock_check_call.call_args)

    @patch('committer.vcs_clients.util.check_call')        
    def test_should_return_false_when_command_is_not_executable (self, mock_check_call):
        vcs_client = VcsClient()
        
        mock_check_call.side_effect = subprocess.CalledProcessError(127, 'command')
        
        actual_result = vcs_client.check_if_is_executable('command', '--version', '--quiet')
        
        self.assertFalse(actual_result)
        self.assertEqual(call(['command', '--version', '--quiet']), mock_check_call.call_args)

    @patch('committer.vcs_clients.util.check_call')        
    def test_should_return_false_when_trying_to_execute_command_fails (self, mock_check_call):
        vcs_client = VcsClient()
        mock_check_call.side_effect = OSError()
        
        actual_result = vcs_client.check_if_is_executable('command', '--version', '--quiet')
        
        self.assertFalse(actual_result)
        self.assertEqual(call(['command', '--version', '--quiet']), mock_check_call.call_args)

    @patch('committer.vcs_clients.util.check_call')        
    def test_should_raise_eception_when_during_check_something_unexpected_happens (self, mock_check_call):
        vcs_client = VcsClient()
        mock_check_call.side_effect = Exception('Not executable')
        
        self.assertRaises(Exception, vcs_client.check_if_is_executable, ('command', '--version', '--quiet'))
        
