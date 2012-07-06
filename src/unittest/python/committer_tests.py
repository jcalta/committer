import unittest

from mock import Mock, call, patch

import committer

class CommitTests (unittest.TestCase):
    
    @patch('committer.increment_version')
    def test_should_pull_from_repository (self, incrementor_mock):
        repository_mock = Mock()
        
        committer.handle_repository(repository_mock, 'This is a message.')
        
        self.assertEquals(call(), repository_mock.pull.call_args)
        
    @patch('committer.increment_version')
    def test_should_increment_version (self, incrementor_mock):
        repository_mock = Mock()
        
        committer.handle_repository(repository_mock, 'This is a message.')
        
        self.assertEquals(call(), incrementor_mock.call_args)
        
    @patch('committer.increment_version')
    def test_should_commit_to_repository (self, incrementor_mock):
        repository_mock = Mock()
        
        committer.handle_repository(repository_mock, 'This is a message.')
        
        self.assertEquals(call('This is a message.'), \
                          repository_mock.commit.call_args)
        
    @patch('committer.increment_version')
    def test_should_push_to_repository (self, incrementor_mock):
        repository_mock = Mock()
        
        committer.handle_repository(repository_mock, 'This is a message.')
        
        self.assertEquals(call(), repository_mock.push.call_args)
        
    @patch('committer.git.Git')
    def test_should_return_new_git_object (self, git_class_mock):
        committer.detect_repository()
        
        self.assertEquals(call(), git_class_mock())

    @patch('sys.exit')
    def test_should_exit_when_no_arguments_given (self, exit_mock):
        committer.main([])
        
        self.assertEquals(call(1), exit_mock.call_args)

    @patch('committer.handle_repository')    
    @patch('committer.detect_repository')
    def test_should_detect_repository (self, \
                                detect_repository_mock, handle_repository_mock):
        detect_repository_mock.return_value = 'repository'
         
        committer.main(['command', 'message'])
        
        self.assertEquals(call(), detect_repository_mock.call_args)
        
    @patch('committer.handle_repository')    
    @patch('committer.detect_repository')
    def test_should_commit_use_first_argument_as_message (self, \
            detect_repository_mock, handle_repository_mock):
        
        detect_repository_mock.return_value = 'repository'
        committer.main(['command', 'message'])
        
        self.assertEquals(call('repository', 'message'), \
                          handle_repository_mock.call_args)
