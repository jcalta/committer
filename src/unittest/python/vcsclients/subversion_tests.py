import unittest

from mock import call, patch

from committer.vcsclients import subversion


class PropertiesTests (unittest.TestCase):
    def test_should_have_command_property (self):
        self.assertEqual('svn', subversion.COMMAND)

    def test_should_have_name_property (self):
        self.assertEqual('Subversion', subversion.NAME)

       
class CommitTests (unittest.TestCase):
    @patch('committer.vcsclients.subversion._svn')
    def test_should_prepend_svn_to_given_arguments (self, mock_svn):
        
        subversion.commit('This is a commit message.')
        
        self.assertEqual(call('commit', '-m', 'This is a commit message.'), mock_svn.call_args)
        
        
class StatusTests (unittest.TestCase):
    @patch('committer.vcsclients.subversion._svn')
    def test_should_call_status (self, mock_svn):
        subversion.status()
        
        self.assertEqual(call('status'), mock_svn.call_args)
        

class UpdateTests (unittest.TestCase):
    @patch('committer.vcsclients.subversion._svn')
    def test_should_call_update (self, mock_svn):
        subversion.update()
        
        self.assertEqual(call('update'), mock_svn.call_args)
        

class DetectTests (unittest.TestCase):
    @patch('os.path.isdir')
    def test_return_false_if_dot_svn_directory_does_not_exist (self, mock_exists):
        mock_exists.return_value = False
        
        actual_return_value = subversion.detect()
        
        self.assertEqual(False, actual_return_value)
        self.assertEqual(call('.svn'), mock_exists.call_args)

    @patch('os.path.isdir')
    def test_return_true_if_dot_svn_directory_exists (self, mock_exists):
        mock_exists.return_value = True
        
        actual_return_value = subversion.detect()
        
        self.assertEqual(True, actual_return_value)
        self.assertEqual(call('.svn'), mock_exists.call_args)


class IsExecutableTests (unittest.TestCase):
    @patch('committer.vcsclients.subversion.check_if_is_executable')
    def test_should_return_value_of_check (self, mock_check):
        mock_check.return_value = 'value from check'
        
        actual_return_value = subversion.is_executable()
        
        self.assertEqual('value from check', actual_return_value)

    @patch('committer.vcsclients.subversion.check_if_is_executable')
    def test_should_check_using_svn_version_quiet (self, mock_check):
        mock_check.return_value = 'value from check'
        
        subversion.is_executable()
        
        self.assertEqual(call('svn', '--version', '--quiet'), mock_check.call_args)


class SubversionTests (unittest.TestCase):
    @patch('committer.vcsclients.subversion.execute_command')
    def test_should_execute_svn_using_arguments (self, mock_execute):
        subversion._svn('arg1', 'arg2', 'arg3')
        
        self.assertEqual(call('svn', 'arg1', 'arg2', 'arg3'), mock_execute.call_args)