from mock import call, patch

import unittest_support

from committer import  handler


class HandlerTests (unittest_support.TestCase):
    @patch('committer.incrementor.increment_version')
    def test_should_pull_from_repository (self, mock_incrementor):
        mock_repository = self.create_mock_repository()
        
        handler.commit(mock_repository, 'This is a message.')
        
        self.assertEquals(call(), mock_repository.update.call_args)

        
    def test_should_not_increment_version (self, mock_incrementor):
        mock_repository = self.create_mock_repository()
        
        handler.commit(mock_repository, 'This is a message.')
        
        self.assertEquals(None, mock_incrementor.call_args)

        
    @patch('committer.incrementor.increment_version')
    def test_should_not_increment_version (self, mock_incrementor):
        repository_mock = self.create_mock_repository()
        
        handler.commit(repository_mock, 'This is a message.', increment=True)
        
        self.assertEquals(call(), mock_incrementor.call_args)

        
    @patch('committer.incrementor.increment_version')
    def test_should_commit_to_repository (self, mock_incrementor):
        repository_mock = self.create_mock_repository()
        
        handler.commit(repository_mock, 'This is a message.')
        
        self.assertEquals(call('This is a message.'), repository_mock.commit.call_args)

        
    @patch('committer.incrementor.increment_version')
    def test_should_return_zero (self, mock_incrementor):
        repository_mock = self.create_mock_repository()
        
        actual_return_code = handler.commit(repository_mock, 'This is a message.')
        
        self.assertEquals(0, actual_return_code)
