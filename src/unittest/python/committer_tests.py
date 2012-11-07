import unittest

from mock import Mock, call, patch

from committer import errors, perform, __doc__ as docstring

class PerformTests (unittest.TestCase):
    @patch('committer.stdout')
    @patch('committer.exit')
    def test_should_exit_directly_if_first_argument_is_version (self, mock_exit, mock_stdout):
        mock_command = Mock()
        mock_command.perform.side_effect = Exception('Perform should never be called.')

        perform(mock_command, ['/usr/local/bin/commit', '--version'])

        self.assertEquals(call('committer version ${version}\n'), mock_stdout.write.call_args)
        self.assertEquals(call(0), mock_exit.call_args)

    @patch('committer.stdout')
    @patch('committer.exit')
    def test_should_exit_and_print_usage_if_first_argument_is_help (self, mock_exit, mock_stdout):
        mock_command = Mock()
        mock_command.perform.side_effect = Exception('Perform should never be called.')

        perform(mock_command, ['/usr/local/bin/commit', 'help'])

        self.assertEquals(call("""
usage:
    commit "message" [++]    commits all changes
    st                       shows all changes
    update                   updates the current directory
"""), mock_stdout.write.call_args)
        self.assertEquals(call(0), mock_exit.call_args)

    @patch('committer.stdout')
    @patch('committer.exit')
    def test_should_call_perform_on_given_command (self, mock_exit, mock_stdout):
        mock_command = Mock()
        arguments = ['/usr/local/bin/commit']

        perform(mock_command, arguments)

        self.assertEquals(call(arguments), mock_command.perform.call_args)
        self.assertEquals(call(0), mock_exit.call_args)

    @patch('committer.stdout')
    @patch('committer.stderr')
    @patch('committer.exit')
    def test_should_return_with_error_message_and_code (self, mock_exit, mock_stderr, mock_stdout):
        mock_command = Mock()
        mock_command.perform.side_effect = errors.CommitterException('Error message.', 123)

        perform(mock_command, ['/usr/local/bin/commit'])

        self.assertEquals(call('Error message.\n'), mock_stderr.write.call_args)
        self.assertEquals(call(123), mock_exit.call_args)
