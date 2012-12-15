import unittest

from mock import Mock, call, patch

from committer import ScriptCommand, errors

class ScriptCommandWrapperTests (unittest.TestCase):
    @patch('committer.stdout')
    @patch('committer.exit')
    def test_should_exit_directly_if_first_argument_is_version (self, mock_exit, mock_stdout):
        mock_command = Mock()
        mock_command.perform.side_effect = Exception('Perform should never be called.')

        ScriptCommand(mock_command)(['/usr/local/bin/commit', '--version'])

        self.assertEqual(call('committer version ${version}\n'), mock_stdout.write.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.stdout')
    @patch('committer.exit')
    def test_should_exit_and_print_usage_if_first_argument_is_help (self, mock_exit, mock_stdout):
        mock_command = Mock()
        mock_command.perform.side_effect = Exception('Perform should never be called.')

        ScriptCommand(mock_command)(['/usr/local/bin/commit', 'help'])

        self.assertEqual(call("""
usage:
    ci "message"     commits all changes
    st               shows all changes
    up               updates the current directory
"""), mock_stdout.write.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.stdout')
    @patch('committer.exit')
    def test_should_call_perform_on_given_command (self, mock_exit, mock_stdout):
        mock_command = Mock()
        arguments = ['/usr/local/bin/commit']

        ScriptCommand(mock_command)(arguments)

        self.assertEqual(call(arguments), mock_command.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.stdout')
    @patch('committer.stderr')
    @patch('committer.exit')
    def test_should_return_with_error_message_and_code (self, mock_exit, mock_stderr, mock_stdout):
        mock_command = Mock()
        mock_command.side_effect = errors.CommitterError('Error message.', 123)

        ScriptCommand(mock_command)(['/usr/local/bin/commit'])

        self.assertEqual(call('Error message.\n'), mock_stderr.write.call_args)
        self.assertEqual(call(123), mock_exit.call_args)
