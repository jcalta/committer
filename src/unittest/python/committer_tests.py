import unittest

from mock import Mock, call, patch

from committer import Configuration, ScriptCommand, errors

USAGE_INFORMATION = """
usage:
    ci "message"     commits all changes
    st               shows all changes
    up               updates the current directory
"""

class ScriptCommandWrapperTests (unittest.TestCase):
    @patch('committer.LOGGER')
    @patch('committer.exit')
    @patch('committer.execute_command')
    def test_should_exit_directly_if_interrupted_by_user (self, mock_execute_command, mock_exit, mock_logger):
        mock_command = Mock()
        mock_command.side_effect = KeyboardInterrupt()

        ScriptCommand(mock_command)(['/usr/local/bin/commit'])

        self.assertEqual(call('Interrupted by user.\n'), mock_logger.error.call_args)
        self.assertEqual(call(1), mock_exit.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    @patch('committer.execute_command')
    def test_should_exit_directly_if_first_argument_is_version (self, mock_execute_command, mock_exit, mock_logger):
        mock_command = Mock()

        ScriptCommand(mock_command)(['/usr/local/bin/commit', '--version'])

        self.assertEqual(call('%s version %s', 'committer', '${version}'), mock_logger.info.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    @patch('committer.execute_command')
    def test_should_exit_directly_if_one_argument_is_version (self, mock_execute_command, mock_exit, mock_logger):
        mock_command = Mock()

        ScriptCommand(mock_command)(['/usr/local/bin/commit', 'hello world', '--version'])

        self.assertEqual(call('%s version %s', 'committer', '${version}'), mock_logger.info.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    @patch('committer.execute_command')
    def test_should_exit_and_print_usage_if_first_argument_is_help (self, mock_execute_command, mock_exit, mock_logger):
        mock_command = Mock()

        ScriptCommand(mock_command)(['/usr/local/bin/commit', 'help'])

        self.assertEqual(call(USAGE_INFORMATION), mock_logger.info.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    @patch('committer.execute_command')
    def test_should_exit_and_print_usage_if_one_argument_is_help (self, mock_execute_command, mock_exit, mock_logger):
        mock_command = Mock()

        ScriptCommand(mock_command)(['/usr/local/bin/commit', 'hello world', 'help'])

        self.assertEqual(call(USAGE_INFORMATION), mock_logger.info.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    @patch('committer.execute_command')
    def test_should_exit_and_print_usage_if_first_argument_is_dashdash_help (self, mock_execute_command, mock_exit, mock_logger):
        mock_command = Mock()

        ScriptCommand(mock_command)(['/usr/local/bin/commit', '--help'])

        self.assertEqual(call(USAGE_INFORMATION), mock_logger.info.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    @patch('committer.execute_command')
    def test_should_exit_and_print_usage_if_one_argument_is_dashdash_help (self, mock_execute_command, mock_exit, mock_logger):
        mock_command = Mock()

        ScriptCommand(mock_command)(['/usr/local/bin/commit', 'hello world', '--help'])

        self.assertEqual(call(USAGE_INFORMATION), mock_logger.info.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    @patch('committer.execute_command')
    def test_should_exit_and_print_usage_if_first_argument_is_dash_h (self, mock_execute_command, mock_exit, mock_logger):
        mock_command = Mock()

        ScriptCommand(mock_command)(['/usr/local/bin/commit', 'hello world', '-h'])

        self.assertEqual(call(USAGE_INFORMATION), mock_logger.info.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    @patch('committer.execute_command')
    def test_should_exit_and_print_usage_if_one_argument_is_dash_h (self, mock_execute_command, mock_exit, mock_logger):
        mock_command = Mock()

        ScriptCommand(mock_command)(['/usr/local/bin/commit', '-h'])

        self.assertEqual(call(USAGE_INFORMATION), mock_logger.info.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    @patch('committer.execute_command')
    @patch('committer.Configuration')
    def test_should_filter_dash_m_argument (self, mock_configuration_class, mock_execute_command, mock_exit, mock_logger):
        mock_configuration = Mock()
        mock_configuration_class.return_value = mock_configuration
        mock_command = Mock()
        arguments = ['/usr/local/bin/commit', '-m', 'Hello world']

        ScriptCommand(mock_command)(arguments)

        self.assertEqual(call(['/usr/local/bin/commit', 'Hello world'], mock_configuration), mock_command.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    @patch('committer.exists')
    @patch('committer.ConfigParser')
    @patch('committer.execute_command')
    def test_should_use_default_configuration_when_no_configuration_file_found (self, mock_execute_command, mock_config_parser_class, mock_exists, mock_exit, mock_logger):
        mock_exists.return_value = False
        mock_command = Mock()
        arguments = ['/usr/local/bin/commit', '-m', 'Hello world']

        ScriptCommand(mock_command)(arguments)

        self.assertEqual(call(".committerrc"), mock_exists.call_args)
        self.assertEqual(None, mock_config_parser_class.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    @patch('committer.exists')
    @patch('committer.ConfigParser')
    @patch('committer.execute_command')
    def test_should_read_configuration_file (self, mock_execute_command, mock_config_parser_class, mock_exists, mock_exit, mock_logger):
        mock_config_parser = Mock()
        mock_config_parser_class.return_value = mock_config_parser
        mock_exists.return_value = True
        mock_command = Mock()
        arguments = ['/usr/local/bin/commit', '-m', 'Hello world']

        ScriptCommand(mock_command)(arguments)

        self.assertEqual(call(".committerrc"), mock_exists.call_args)
        self.assertEqual(call(), mock_config_parser_class.call_args)
        self.assertEqual(call(".committerrc"), mock_config_parser.read.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    @patch('committer.exists')
    @patch('committer.ConfigParser')
    @patch('committer.execute_command')
    def test_should_check_if_execute_before_option_in_configuration_file (self, mock_execute_command, mock_config_parser_class, mock_exists, mock_exit, mock_logger):
        mock_config_parser = Mock()
        mock_config_parser_class.return_value = mock_config_parser
        mock_exists.return_value = True
        mock_command = Mock()
        arguments = ['/usr/local/bin/commit', '-m', 'Hello world']

        ScriptCommand(mock_command)(arguments)

        self.assertEqual(call("DEFAULT", "execute_before"), mock_config_parser.has_option.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    @patch('committer.exists')
    @patch('committer.ConfigParser')
    @patch('committer.execute_command')
    def test_should_get_execute_before_option_from_configuration_file (self, mock_execute_command, mock_config_parser_class, mock_exists, mock_exit, mock_logger):
        mock_config_parser = Mock()
        mock_config_parser_class.return_value = mock_config_parser
        mock_exists.return_value = True
        mock_command = Mock()
        arguments = ['/usr/local/bin/commit', '-m', 'Hello world']

        ScriptCommand(mock_command)(arguments)

        self.assertEqual(call("DEFAULT", "execute_before"), mock_config_parser.get.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    @patch('committer.ScriptCommand._read_configuration_file')
    @patch('committer.execute_command')
    def test_should_execute_configured_command (self, mock_execute_command, mock_read_configuration_file, mock_exit, mock_logger):
        mock_read_configuration_file.return_value = Configuration()
        mock_command = Mock()
        arguments = ['/usr/local/bin/commit']

        ScriptCommand(mock_command)(arguments)

        self.assertEqual(None, mock_execute_command.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    @patch('committer.ScriptCommand._read_configuration_file')
    @patch('committer.execute_command')
    def test_should_not_execute_any_commands_if_no_configuration_file_has_been_loaded (self, mock_execute_command, mock_read_configuration_file, mock_exit, mock_logger):
        mock_read_configuration_file.return_value = Configuration()
        mock_command = Mock()
        arguments = ['/usr/local/bin/commit']

        ScriptCommand(mock_command)(arguments)

        self.assertEqual(None, mock_execute_command.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    @patch('committer.execute_command')
    @patch('committer.Configuration')
    def test_should_execute_given_command_function (self, mock_configuration_class, mock_execute_command, mock_exit, mock_logger):
        mock_configuration = Mock()
        mock_configuration_class.return_value = mock_configuration
        mock_command = Mock()
        arguments = ['/usr/local/bin/commit']

        ScriptCommand(mock_command)(arguments)

        self.assertEqual(call(arguments, mock_configuration), mock_command.call_args)
        self.assertEqual(call(0), mock_exit.call_args)

    @patch('committer.LOGGER')
    @patch('committer.exit')
    @patch('committer.execute_command')
    def test_should_return_with_error_message_and_code (self, mock_execute_command, mock_exit, mock_logger):
        mock_command = Mock()
        mock_command.side_effect = errors.CommitterError('Error message.', 123)

        ScriptCommand(mock_command)(['/usr/local/bin/commit'])

        self.assertEqual(call('Error message.\n'), mock_logger.error.call_args)
        self.assertEqual(call(123), mock_exit.call_args)
