import unittest
import subprocess

from mock import Mock, call, patch

from committer.repositories import mercurial


class MercurialTests (unittest.TestCase):
    def test_should_have_command_property (self):
        self.assertEquals('hg', mercurial.COMMAND)


    def test_should_have_name_property (self):
        self.assertEquals('Mercurial', mercurial.NAME)


    @patch('committer.repositories.mercurial.call')        
    def test_should_call_hg_in_subprocess (self, mock_call):
        mercurial._hg()
        
        self.assertEquals(call(['hg']), mock_call.call_args)


    @patch('committer.repositories.mercurial.call')        
    def test_should_call_hg_using_given_arguments (self, mock_call):
        mercurial._hg('1', '2', '3')
        args = (['hg', '1', '2', '3'])
        self.assertEquals(call(args), mock_call.call_args)
        
        
    @patch('committer.repositories.mercurial._hg')
    def test_should_prepend_hg_to_given_arguments (self, mock_hg):
        
        mercurial.commit('This is a commit message.')
        
        self.assertEquals([call('commit', '-m', 'This is a commit message.'),
                           call('push')],
                          mock_hg.call_args_list)
        
        
    @patch('committer.repositories.mercurial._hg')
    def test_should_call_pull_and_update (self, mock_hg):
        mercurial.update()
        
        self.assertEquals([call('pull'), call('update')], mock_hg.call_args_list)
        

    @patch('committer.repositories.mercurial.check_call')        
    def test_should_return_true_when_hg_is_executable (self, mock_check_call):
        actual_result = mercurial.is_executable()
        
        self.assertTrue(actual_result)
        self.assertEquals(call(['hg', '--version', '--quiet']), mock_check_call.call_args)


    @patch('committer.repositories.mercurial.check_call')        
    def test_should_return_false_when_hg_is_not_executable (self, mock_check_call):
        mock_check_call.side_effect = subprocess.CalledProcessError(127, 'hg')
        
        actual_result = mercurial.is_executable()
        
        self.assertFalse(actual_result)
        self.assertEquals(call(['hg', '--version', '--quiet']), mock_check_call.call_args)


    @patch('committer.repositories.mercurial.check_call')        
    def test_should_raise_eception_when_during_check_something_unexpected_happens (self, mock_check_call):
        mock_check_call.side_effect = Exception('Not executable')
        
        self.assertRaises(Exception, mercurial.is_executable, ())
        

    @patch('os.path.isdir')
    def test_return_false_if_dot_hg_directory_does_not_exist (self, mock_exists):
        mock_exists.return_value = False
        
        actual_return_value = mercurial.detect()
        
        self.assertEquals(False, actual_return_value)
        self.assertEquals(call('.hg'), mock_exists.call_args)

        
    @patch('os.path.isdir')
    def test_return_true_if_dot_hg_directory_exists (self, mock_exists):
        mock_exists.return_value = True
        
        actual_return_value = mercurial.detect()
        
        self.assertEquals(True, actual_return_value)
        self.assertEquals(call('.hg'), mock_exists.call_args)
        