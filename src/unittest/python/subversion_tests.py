import unittest
import subprocess

from mock import Mock, call, patch

from committer.repositories import subversion


class SubversionTests (unittest.TestCase):
    def test_should_have_command_property (self):
        self.assertEquals('svn', subversion.COMMAND)


    def test_should_have_name_property (self):
        self.assertEquals('Subversion', subversion.NAME)


    @patch('committer.repositories.subversion.call')        
    def test_should_call_svn_in_subprocess (self, mock_call):
        subversion._svn()
        
        self.assertEquals(call(['svn']), mock_call.call_args)


    @patch('committer.repositories.subversion.call')        
    def test_should_call_svn_using_given_arguments (self, mock_call):
        subversion._svn('1', '2', '3')
        args = (['svn', '1', '2', '3'])
        self.assertEquals(call(args), mock_call.call_args)
        
        
    @patch('committer.repositories.subversion._svn')
    def test_should_prepend_svn_to_given_arguments (self, mock_svn):
        
        subversion.commit('This is a commit message.')
        
        self.assertEquals(call('commit', '-m', 'This is a commit message.'), mock_svn.call_args)
        
        
    @patch('committer.repositories.subversion._svn')
    def test_should_call_pull_and_update (self, mock_svn):
        subversion.update()
        
        self.assertEquals(call('update'), mock_svn.call_args)
        

    @patch('committer.repositories.subversion.check_call')        
    def test_should_return_true_when_svn_is_executable (self, mock_check_call):
        actual_result = subversion.is_executable()
        
        self.assertTrue(actual_result)
        self.assertEquals(call(['svn', '--version', '--quiet']), mock_check_call.call_args)


    @patch('committer.repositories.subversion.check_call')        
    def test_should_return_false_when_svn_is_not_executable (self, mock_check_call):
        mock_check_call.side_effect = subprocess.CalledProcessError(127, 'svn')
        
        actual_result = subversion.is_executable()
        
        self.assertFalse(actual_result)
        self.assertEquals(call(['svn', '--version', '--quiet']), mock_check_call.call_args)


    @patch('committer.repositories.subversion.check_call')        
    def test_should_raise_eception_when_during_check_something_unexpected_happens (self, mock_check_call):
        mock_check_call.side_effect = Exception('Not executable')
        
        self.assertRaises(Exception, subversion.is_executable, ())
        

    @patch('os.path.isdir')
    def test_return_false_if_dot_svn_directory_does_not_exist (self, mock_exists):
        mock_exists.return_value = False
        
        actual_return_value = subversion.detect()
        
        self.assertEquals(False, actual_return_value)
        self.assertEquals(call('.svn'), mock_exists.call_args)

        
    @patch('os.path.isdir')
    def test_return_true_if_dot_svn_directory_exists (self, mock_exists):
        mock_exists.return_value = True
        
        actual_return_value = subversion.detect()
        
        self.assertEquals(True, actual_return_value)
        self.assertEquals(call('.svn'), mock_exists.call_args)
        