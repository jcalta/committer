import unittest
import subprocess

from mock import Mock, call, patch

from committer.vcsclients import mercurial


class PropertiesTests (unittest.TestCase):
    def test_should_have_command_property (self):
        self.assertEquals('hg', mercurial.COMMAND)


    def test_should_have_name_property (self):
        self.assertEquals('Mercurial', mercurial.NAME)


class CommitTests (unittest.TestCase):
    @patch('committer.vcsclients.mercurial._hg')
    def test_should_prepend_hg_to_given_arguments (self, mock_hg):
        
        mercurial.commit('This is a commit message.')
        
        self.assertEquals([call('commit', '-m', 'This is a commit message.'),
                           call('push')],
                          mock_hg.call_args_list)
        
        
class UpdateTests (unittest.TestCase):
    @patch('committer.vcsclients.mercurial._hg')
    def test_should_call_pull_and_update (self, mock_hg):
        mercurial.update()
        
        self.assertEquals([call('pull'), call('update')], mock_hg.call_args_list)
        

class DetectTests (unittest.TestCase):
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


class IsExecutableTests (unittest.TestCase):
    @patch('committer.vcsclients.mercurial.check_if_is_executable')
    def test_should_return_value_of_check (self, mock_check):
        mock_check.return_value = 'value from check'
        
        actual_return_value = mercurial.is_executable()
        
        self.assertEquals('value from check', actual_return_value)


    @patch('committer.vcsclients.mercurial.check_if_is_executable')
    def test_should_check_using_hg_version_quiet (self, mock_check):
        mock_check.return_value = 'value from check'
        
        mercurial.is_executable()
        
        self.assertEquals(call('hg', '--version', '--quiet'), mock_check.call_args)


class MercurialTests (unittest.TestCase):
    @patch('committer.vcsclients.mercurial.execute_command')
    def test_should_execute_hg_using_arguments (self, mock_execute):
        mercurial._hg('arg1', 'arg2', 'arg3')
        
        self.assertEquals(call('hg', 'arg1', 'arg2', 'arg3'), mock_execute.call_args)
