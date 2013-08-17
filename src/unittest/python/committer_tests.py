import unittest

from mock import Mock, call, patch

from committer import ScriptCommand, errors

USAGE_INFORMATION = """
usage:
    ci "message"     commits all changes
    st               shows all changes
    up               updates the current directory
"""

class ScriptCommandWrapperTests (unittest.TestCase):
    @patch('committer.LOGGER')
    @patch('committer.exit')
    def test_should_exit_directly_if_interrupted_by_user (self, mock_exit, mock_logger):
        mock_command = Mock()
        mock_command.side_effect = KeyboardInterrupt()

        ScriptCommand(mock_command)(['/usr/local/bin/commit'])

        self.assertEqual(call('Interrupted by user.\n'), mock_logger.error.call_args)
        self.assertEqual(call(1), mock_exit.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    def test_should_exit_directly_if_first_argument_is_version (self, mock_exit, mock_logger):
        mock_command = Mock()

        ScriptCommand(mock_command)(['/usr/local/bin/commit', '--version'])

        self.assertEqual(call('%s version %s', 'committer', '${version}'), mock_logger.info.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    def test_should_exit_directly_if_one_argument_is_version (self, mock_exit, mock_logger):
        mock_command = Mock()

        ScriptCommand(mock_command)(['/usr/local/bin/commit', 'hello world', '--version'])

        self.assertEqual(call('%s version %s', 'committer', '${version}'), mock_logger.info.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    def test_should_exit_and_print_usage_if_first_argument_is_help (self, mock_exit, mock_logger):
        mock_command = Mock()

        ScriptCommand(mock_command)(['/usr/local/bin/commit', 'help'])

        self.assertEqual(call(USAGE_INFORMATION), mock_logger.info.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    def test_should_exit_and_print_usage_if_one_argument_is_help (self, mock_exit, mock_logger):
        mock_command = Mock()

        ScriptCommand(mock_command)(['/usr/local/bin/commit', 'hello world', 'help'])

        self.assertEqual(call(USAGE_INFORMATION), mock_logger.info.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    def test_should_exit_and_print_usage_if_first_argument_is_dashdash_help (self, mock_exit, mock_logger):
        mock_command = Mock()

        ScriptCommand(mock_command)(['/usr/local/bin/commit', '--help'])

        self.assertEqual(call(USAGE_INFORMATION), mock_logger.info.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    def test_should_exit_and_print_usage_if_one_argument_is_dashdash_help (self, mock_exit, mock_logger):
        mock_command = Mock()

        ScriptCommand(mock_command)(['/usr/local/bin/commit', 'hello world', '--help'])

        self.assertEqual(call(USAGE_INFORMATION), mock_logger.info.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    def test_should_exit_and_print_usage_if_first_argument_is_dash_h (self, mock_exit, mock_logger):
        mock_command = Mock()

        ScriptCommand(mock_command)(['/usr/local/bin/commit', 'hello world', '-h'])

        self.assertEqual(call(USAGE_INFORMATION), mock_logger.info.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    def test_should_exit_and_print_usage_if_one_argument_is_dash_h (self, mock_exit, mock_logger):
        mock_command = Mock()

        ScriptCommand(mock_command)(['/usr/local/bin/commit', '-h'])

        self.assertEqual(call(USAGE_INFORMATION), mock_logger.info.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    def test_should_filter_dash_m_argument (self, mock_exit, mock_logger):
        mock_command = Mock()
        arguments = ['/usr/local/bin/commit', '-m', 'Hello world']

        ScriptCommand(mock_command)(arguments)

        self.assertEqual(call(['/usr/local/bin/commit', 'Hello world']), mock_command.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    def test_should_call_perform_on_given_command (self, mock_exit, mock_logger):
        mock_command = Mock()
        arguments = ['/usr/local/bin/commit']

        ScriptCommand(mock_command)(arguments)

        self.assertEqual(call(arguments), mock_command.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    def test_should_return_with_error_message_and_code (self, mock_exit, mock_logger):
        mock_command = Mock()
        mock_command.side_effect = errors.CommitterError('Error message.', 123)

        ScriptCommand(mock_command)(['/usr/local/bin/commit'])

        self.assertEqual(call('Error message.\n'), mock_logger.error.call_args)
        self.assertEqual(call(123), mock_exit.call_args)
