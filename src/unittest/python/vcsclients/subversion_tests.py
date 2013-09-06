import unittest

from mockito import when, verify, unstub, any as any_value

import committer
from committer.vcsclients.subversion import SubversionClient


class SubversionClientTests (unittest.TestCase):
    def setUp(self):
        self.subversion_client = SubversionClient()
    
    def tearDown(self):
        unstub()
    
    def test_should_have_command_property (self):
        self.assertEqual('svn', self.subversion_client.command)

    def test_should_have_name_property (self):
        self.assertEqual('Subversion', self.subversion_client.name)

    def test_should_prepend_svn_to_given_arguments (self):
        when(self.subversion_client)._svn(any_value(), any_value(), any_value()).thenReturn(None)
        
        self.subversion_client.commit('This is a commit message.')
        
        verify(self.subversion_client)._svn('commit', '-m', 'This is a commit message.')
        
    def test_should_call_status (self):
        when(self.subversion_client)._svn(any_value()).thenReturn(None)
        
        self.subversion_client.status()
        
        verify(self.subversion_client)._svn('status')

    def test_should_call_update (self):
        when(self.subversion_client)._svn(any_value()).thenReturn(None)

        self.subversion_client.update()
        
        verify(self.subversion_client)._svn('update')
        
    def test_should_store_update_result (self):
        when(self.subversion_client)._svn(any_value()).thenReturn({'stdout': 'abc', 'stderr': 'err', 'returncode': 123})

        self.subversion_client.update()
        
        self.assertEqual({'stdout': 'abc', 'stderr': 'err', 'returncode': 123}, self.subversion_client._update_result)
        
    def test_return_false_if_dot_svn_directory_does_not_exist (self):
        when(committer.vcsclients.subversion.path).isdir(any_value()).thenReturn(False)
        
        actual_return_value = self.subversion_client.detect()
        
        self.assertEqual(False, actual_return_value)
        verify(committer.vcsclients.subversion.path).isdir('.svn')

    def test_return_true_if_dot_svn_directory_exists (self):
        when(committer.vcsclients.subversion.path).isdir(any_value()).thenReturn(True)
        
        actual_return_value = self.subversion_client.detect()
        
        self.assertEqual(True, actual_return_value)
        verify(committer.vcsclients.subversion.path).isdir('.svn')

    def test_should_return_value_of_check (self):
        when(committer.vcsclients.subversion).check_if_is_executable(any_value(), any_value(), any_value()).thenReturn('value from check')
        
        actual_return_value = self.subversion_client.is_executable()
        
        self.assertEqual('value from check', actual_return_value)
        verify(committer.vcsclients.subversion).check_if_is_executable('svn', '--version', '--quiet')


    def test_should_execute_svn_using_arguments (self):
        when(committer.vcsclients.subversion).execute_command(any_value(), any_value(), any_value(), any_value()).thenReturn(None)
        
        self.subversion_client._svn('arg1', 'arg2', 'arg3')
        
        verify(committer.vcsclients.subversion).execute_command('svn', 'arg1', 'arg2', 'arg3')

    def test_should_return_execution_result (self):
        when(committer.vcsclients.subversion).execute_command(any_value(), any_value(), any_value(), any_value()).thenReturn({'stdout': 'abc', 'stderr': 'err', 'returncode': 123})
        
        actual_result = self.subversion_client._svn('arg1', 'arg2', 'arg3')
        
        self.assertEqual({'stdout': 'abc', 'stderr': 'err', 'returncode': 123}, actual_result)

    def test_should_return_false_if_last_update_found_updates(self):
        self.subversion_client._update_result = {'stdout': 'Found updates ... blabla'}
        
        actual = self.subversion_client.everything_was_up_to_date
        
        self.assertFalse(actual)
        
    def test_should_return_true_if_everything_is_up_to_date(self):
        self.subversion_client._update_result = {'stdout': "At revision 333."}

        actual = self.subversion_client.everything_was_up_to_date
        
        self.assertTrue(actual)
