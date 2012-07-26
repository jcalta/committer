import unittest
import subprocess

from mock import Mock, call, patch

from committer.repositories import git


class GitTests (unittest.TestCase):
    def test_should_have_command_property (self):
        self.assertEquals('git', git.COMMAND)


    def test_should_have_name_property (self):
        self.assertEquals('Git', git.NAME)


    @patch('committer.repositories.git.call')        
    def test_should_call_git_in_subprocess (self, mock_call):
        git._git()
        
        self.assertEquals(call(['git']), mock_call.call_args)


    @patch('committer.repositories.git.call')        
    def test_should_call_git_using_given_arguments (self, mock_call):
        git._git('1', '2', '3')
        args = (['git', '1', '2', '3'])
        self.assertEquals(call(args), mock_call.call_args)
        
        
    @patch('committer.repositories.git._git')
    def test_should_prepend_git_to_given_arguments (self, mock_git):
        
        git.commit('This is a commit message.')
        
        self.assertEquals([call('commit', '-a', '-m', 'This is a commit message.'),
                           call('push')],
                          mock_git.call_args_list)
        
        
    @patch('committer.repositories.git._git')
    def test_should_call_pull (self, mock_git):
        git.update()
        
        self.assertEquals(call('pull'), mock_git.call_args)
        

    @patch('committer.repositories.git.check_call')        
    def test_should_return_true_when_git_is_executable (self, mock_check_call):
        actual_result = git.is_executable()
        
        self.assertTrue(actual_result)
        self.assertEquals(call(['git', '--version']), mock_check_call.call_args)


    @patch('committer.repositories.git.check_call')        
    def test_should_return_false_when_git_is_not_executable (self, mock_check_call):
        mock_check_call.side_effect = subprocess.CalledProcessError(127, 'git')
        
        actual_result = git.is_executable()
        
        self.assertFalse(actual_result)
        self.assertEquals(call(['git', '--version']), mock_check_call.call_args)


    @patch('committer.repositories.git.check_call')        
    def test_should_raise_eception_when_during_check_something_unexpected_happens (self, mock_check_call):
        mock_check_call.side_effect = Exception('Not executable')
        
        self.assertRaises(Exception, git.is_executable, ())
        

    @patch('os.path.isdir')
    def test_return_false_if_dot_git_directory_does_not_exist (self, mock_exists):
        mock_exists.return_value = False
        
        actual_return_value = git.detect()
        
        self.assertEquals(False, actual_return_value)
        self.assertEquals(call('.git'), mock_exists.call_args)

        
    @patch('os.path.isdir')
    def test_return_true_if_dot_git_directory_exists (self, mock_exists):
        mock_exists.return_value = True
        
        actual_return_value = git.detect()
        
        self.assertEquals(True, actual_return_value)
        self.assertEquals(call('.git'), mock_exists.call_args)
        