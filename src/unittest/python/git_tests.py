import unittest

from mock import (call,
                  patch,
                  Mock)

from committer.repository import git


class GitTests (unittest.TestCase):
    @patch('committer.repository.git.subprocess')        
    def test_should_call_git_in_subprocess (self, subprocess_mock):
        git._git()
        
        self.assertEquals(call(['git']), subprocess_mock.call.call_args)

    @patch('committer.repository.git.subprocess')        
    def test_should_call_git_using_given_arguments (self, subprocess_mock):
        git._git('1', '2', '3')
        args = (['git', '1', '2', '3'])
        self.assertEquals(call(args), subprocess_mock.call.call_args)
        
    @patch('committer.repository.git._git')
    def test_should_prepend_git_to_given_arguments (self, git_mock):
        
        git.commit('This is a commit message.')
        
        self.assertEquals( \
                    call('commit', '-a', '-m', 'This is a commit message.'), \
                    git_mock.call_args)

    @patch('committer.repository.git._git')
    def test_should_call_git_pull (self, git_mock):
        git.pull()
        
        self.assertEquals(call('pull'), git_mock.call_args)

    @patch('committer.repository.git._git')
    def test_should_call_git_push (self, git_mock):
        git.push()
        
        self.assertEquals(call('push'), git_mock.call_args)

    @patch('committer.repository.git.subprocess')        
    def test_should_execute_check_call_on_git_version (self, subprocess_mock):
        git._ensure_git_is_executable()
        
        self.assertEquals(call(['git', '--version']), subprocess_mock.check_call.call_args)
