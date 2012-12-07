import unittest

from mockito import when, verify, unstub, any as any_value

from committer.vcsclients.mercurial import MercurialClient
import committer


class MercurialClientTests (unittest.TestCase):
    def setUp(self):
        self.mercurial_client = MercurialClient()
    
    def tearDown(self):
        unstub()
     
    def test_should_have_command_property (self):
        self.assertEqual('hg', self.mercurial_client.command)

    def test_should_have_name_property (self):
        self.assertEqual('Mercurial', self.mercurial_client.name)

    def test_should_prepend_hg_to_given_arguments (self):
        when(self.mercurial_client)._hg(any_value(), any_value(), any_value()).thenReturn(None)
        when(self.mercurial_client)._hg(any_value()).thenReturn(None)
        
        self.mercurial_client.commit('This is a commit message.')
        
        verify(self.mercurial_client)._hg('commit', '-m', 'This is a commit message.')
        verify(self.mercurial_client)._hg('push')
        
    def test_should_call_pull_and_update (self):
        when(self.mercurial_client)._hg(any_value()).thenReturn(None)
        
        self.mercurial_client.update()
        
        verify(self.mercurial_client)._hg('pull')
        verify(self.mercurial_client)._hg('update')
        
    def test_should_call_status (self):
        when(self.mercurial_client)._hg(any_value()).thenReturn(None)
        
        self.mercurial_client.status()
        
        verify(self.mercurial_client)._hg('status')
        

    def test_return_false_if_dot_hg_directory_does_not_exist (self):
        when(committer.vcsclients.mercurial.path).isdir(any_value()).thenReturn(False)
        
        actual_return_value = self.mercurial_client.detect()
        
        self.assertEqual(False, actual_return_value)
        when(committer.vcsclients.mercurial.path).isdir('.hg')

    def test_return_true_if_dot_hg_directory_exists (self):
        when(committer.vcsclients.mercurial.path).isdir(any_value()).thenReturn(True)
        
        actual_return_value = self.mercurial_client.detect()
        
        self.assertEqual(True, actual_return_value)
        when(committer.vcsclients.mercurial.path).isdir('.hg')


    def test_should_return_value_of_check (self):
        when(self.mercurial_client).check_if_is_executable(any_value(), any_value(), any_value()).thenReturn('value from check')
        
        actual_return_value = self.mercurial_client.is_executable()
        
        self.assertEqual('value from check', actual_return_value)
        verify(self.mercurial_client).check_if_is_executable('hg', '--version', '--quiet')


    def test_should_execute_hg_using_arguments (self):
        when(self.mercurial_client).execute_command(any_value(), any_value(), any_value(), any_value()).thenReturn(None)
        
        self.mercurial_client._hg('arg1', 'arg2', 'arg3')
        
        verify(self.mercurial_client).execute_command('hg', 'arg1', 'arg2', 'arg3')
