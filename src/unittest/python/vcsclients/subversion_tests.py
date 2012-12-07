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
        self.assertEqual('svn', self.subversion_client.COMMAND)

    def test_should_have_name_property (self):
        self.assertEqual('Subversion', self.subversion_client.NAME)

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
        when(self.subversion_client).check_if_is_executable(any_value(), any_value(), any_value()).thenReturn('value from check')
        
        actual_return_value = self.subversion_client.is_executable()
        
        self.assertEqual('value from check', actual_return_value)
        verify(self.subversion_client).check_if_is_executable('svn', '--version', '--quiet')


    def test_should_execute_svn_using_arguments (self):
        when(self.subversion_client).execute_command(any_value(), any_value(), any_value(), any_value()).thenReturn(None)
        
        self.subversion_client._svn('arg1', 'arg2', 'arg3')
        
        verify(self.subversion_client).execute_command('svn', 'arg1', 'arg2', 'arg3')
