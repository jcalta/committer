import unittest

from mock import Mock, call, patch

import committer


class CommitTests (unittest.TestCase):
    @patch('committer.increment_version')
    def test_should_pull_from_repository (self, mock_incrementor):
        mock_repository = self.create_mock_repository()
        
        committer.handle_repository(mock_repository, 'This is a message.')
        
        self.assertEquals(call(), mock_repository.pull.call_args)
        
    def test_should_not_increment_version (self, mock_incrementor):
        mock_repository = self.create_mock_repository()
        
        committer.handle_repository(mock_repository, 'This is a message.')
        
        self.assertEquals(None, mock_incrementor.call_args)
        
    @patch('committer.increment_version')
    def test_should_not_increment_version (self, mock_incrementor):
        repository_mock = self.create_mock_repository()
        
        committer.handle_repository(repository_mock, 'This is a message.', increment=True)
        
        self.assertEquals(call(), mock_incrementor.call_args)
        
    @patch('committer.increment_version')
    def test_should_commit_to_repository (self, mock_incrementor):
        repository_mock = self.create_mock_repository()
        
        committer.handle_repository(repository_mock, 'This is a message.')
        
        self.assertEquals(call('This is a message.'), repository_mock.commit.call_args)
        
    @patch('committer.increment_version')
    def test_should_push_to_repository (self, mock_incrementor):
        repository_mock = self.create_mock_repository()
        
        committer.handle_repository(repository_mock, 'This is a message.')
        
        self.assertEquals(call(), repository_mock.push.call_args)
        
    @patch('sys.exit')
    @patch('sys.stdout')
    def test_should_exit_when_no_arguments_given (self, mock_stdout, mock_exit):
        committer.main([])
        
        self.assertEquals(call(1), mock_exit.call_args)

    @patch('committer.handle_repository')    
    @patch('committer.repositories.detect')
    @patch('sys.stdout')
    def test_should_detect_repository (self, mock_stdout, mock_detect_repository, mock_handle_repository):
        mock_repository = self.create_mock_repository()
        mock_detect_repository.return_value = [mock_repository]
         
        committer.main(['command', 'message'])
        
        self.assertEquals(call(), mock_detect_repository.call_args)
        
    @patch('committer.handle_repository')    
    @patch('committer.repositories.detect')
    @patch('sys.stdout')
    def test_should_commit_use_first_argument_as_message (self, mock_stdout, mock_detect_repository, mock_handle_repository):
        mock_repository = self.create_mock_repository()
        mock_detect_repository.return_value = [mock_repository]
        committer.main(['command', 'message'])
        
        self.assertEquals(call(mock_repository, 'message'), mock_handle_repository.call_args)

    @patch('committer.handle_repository')    
    @patch('committer.repositories.detect')
    @patch('sys.stdout')
    def test_should_commit_and_increment_when_second_argument_is_plus_plus (self, mock_stdout, mock_detect, mock_handle_repository):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        
        committer.main(['command', 'message', '++'])
        
        self.assertEquals(call(mock_repository, 'message', increment=True), mock_handle_repository.call_args)
    
    @patch('sys.exit')    
    @patch('committer.repositories.detect')
    @patch('sys.stdout')
    def test_should_exit_when_no_repository_could_be_detected (self, mock_stdout, mock_detect, mock_exit):
        mock_detect.return_value = []
        
        committer.main(['command', 'message', '++'])
        
        self.assertEquals(call(1), mock_exit.call_args)
        
    @patch('sys.exit')    
    @patch('committer.repositories.detect')
    @patch('sys.stdout')
    def test_should_exit_when_more_than_one_repository_have_been_detected (self, mock_stdout, mock_detect, mock_exit):
        mock_detect.return_value = [self.create_mock_repository(), self.create_mock_repository()]
        
        committer.main(['command', 'message', '++'])
        
        self.assertEquals(call(1), mock_exit.call_args)

    def create_mock_repository (self):
        mock_repository = Mock()
        mock_repository.NAME = 'mocked-repository'
        return mock_repository