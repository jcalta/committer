import unittest
import subprocess

from mock import Mock, call, patch

from committer.repositories import subversion


class SubversionTests (unittest.TestCase):
    def test_should_have_command_property (self):
        self.assertEquals('svn', subversion.COMMAND)


    def test_should_have_name_property (self):
        self.assertEquals('Subversion', subversion.NAME)

       
    @patch('committer.repositories.subversion._svn')
    def test_should_prepend_svn_to_given_arguments (self, mock_svn):
        
        subversion.commit('This is a commit message.')
        
        self.assertEquals(call('commit', '-m', 'This is a commit message.'), mock_svn.call_args)
        
        
    @patch('committer.repositories.subversion._svn')
    def test_should_call_pull_and_update (self, mock_svn):
        subversion.update()
        
        self.assertEquals(call('update'), mock_svn.call_args)
        


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


    @patch('committer.repositories.subversion.check_if_is_executable')
    def test_should_return_value_of_check (self, mock_check):
        mock_check.return_value = 'value from check'
        
        actual_return_value = subversion.is_executable()
        
        self.assertEquals('value from check', actual_return_value)


    @patch('committer.repositories.subversion.check_if_is_executable')
    def test_should_check_using_svn_version_quiet (self, mock_check):
        mock_check.return_value = 'value from check'
        
        subversion.is_executable()
        
        self.assertEquals(call('svn', '--version', '--quiet'), mock_check.call_args)


    @patch('committer.repositories.subversion.execute_command')
    def test_should_execute_svn_using_arguments (self, mock_execute):
        subversion._svn('arg1', 'arg2', 'arg3')
        
        self.assertEquals(call('svn', 'arg1', 'arg2', 'arg3'), mock_execute.call_args)