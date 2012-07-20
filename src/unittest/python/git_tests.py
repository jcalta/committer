import unittest

from mock import Mock, call, patch

from committer.repository import git


class GitTests (unittest.TestCase):
    @patch('committer.repository.git.subprocess')        
    def test_should_call_git_in_subprocess (self, mock_subprocess):
        git._git()
        
        self.assertEquals(call(['git']), mock_subprocess.call.call_args)

    @patch('committer.repository.git.subprocess')        
    def test_should_call_git_using_given_arguments (self, mock_subprocess):
        git._git('1', '2', '3')
        args = (['git', '1', '2', '3'])
        self.assertEquals(call(args), mock_subprocess.call.call_args)
        
    @patch('committer.repository.git._git')
    def test_should_prepend_git_to_given_arguments (self, mock_git):
        
        git.commit('This is a commit message.')
        
        self.assertEquals(call('commit', '-a', '-m', 'This is a commit message.'), mock_git.call_args)

    @patch('committer.repository.git._git')
    def test_should_call_git_pull (self, mock_git):
        git.pull()
        
        self.assertEquals(call('pull'), mock_git.call_args)

    @patch('committer.repository.git._git')
    def test_should_call_git_push (self, mock_git):
        git.push()
        
        self.assertEquals(call('push'), mock_git.call_args)

    @patch('committer.repository.git.subprocess')        
    def test_should_execute_check_call_on_git_version (self, mock_subprocess):
        git._ensure_git_is_executable()
        
        self.assertEquals(call(['git', '--version']), mock_subprocess.check_call.call_args)

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
        