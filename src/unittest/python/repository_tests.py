import unittest

from mock import Mock, call, patch

from committer.repository import Git

class GitTests (unittest.TestCase):
    def test_should_test_if_git_is_executable (self):
        git_mock = Mock(Git)
        git_mock._ensure_git_is_executable.return_value = None 
        
        Git.__init__(git_mock)
        
        self.assertEquals(call(), git_mock._ensure_git_is_executable.call_args)
    
    @patch('committer.repository.subprocess')        
    def test_should_call_git_in_subprocess (self, subprocess_mock):
        git_mock = Mock(Git)
        
        Git._git(git_mock)
        
        self.assertEquals(call(['git']), subprocess_mock.call.call_args)

    @patch('committer.repository.subprocess')        
    def test_should_call_git_using_given_arguments (self, subprocess_mock):
        git_mock = Mock(Git)
        
        Git._git(git_mock, '1', '2', '3')
        args = (['git', '1', '2', '3'])
        self.assertEquals(call(args), subprocess_mock.call.call_args)
        
    def test_should_prepend_git_to_given_arguments (self):
        git_mock = Mock(Git)
        
        Git.commit(git_mock, 'This is a commit message.')
        
        self.assertEquals(call('commit', '-a', '-m', 'This is a commit message.'), git_mock._git.call_args)

    def test_should_call_git_pull (self):
        git_mock = Mock(Git)
        
        Git.pull(git_mock)
        
        self.assertEquals(call('pull'), git_mock._git.call_args)

    def test_should_call_git_push (self):
        git_mock = Mock(Git)
        
        Git.push(git_mock)
        
        self.assertEquals(call('push'), git_mock._git.call_args)

    @patch('committer.repository.subprocess')        
    def test_should_execute_check_call_on_git_version (self, subprocess_mock):
        git_mock = Mock(Git)
        
        Git._ensure_git_is_executable(git_mock)
        
        self.assertEquals(call(['git', '--version']), subprocess_mock.check_call.call_args)
        