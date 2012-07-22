from mock import call, patch

import committer
import unittest_support


class CommitterTests (unittest_support.TestCase):
    @patch('sys.stderr')
    def test_should_return_one (self, mock_stderr):
        actual_return_code = committer.error('Something went wrong.')
        
        self.assertEquals(1, actual_return_code)
        
    @patch('sys.stderr')
    def test_should_write_given_message_to_stderr (self, mock_stderr):
        committer.error('Failed.')
        
        self.assertEquals(call('Failed.'), mock_stderr.write.call_args)
    
    @patch('committer.error', return_value=5)
    def test_should_exit_when_no_arguments_given (self, mock_error):
        actual_return_code = committer.main(['commit'])
        
        self.assertEquals(5, actual_return_code)

    @patch('committer.handler.commit')    
    @patch('committer.repositories.detect')
    def test_should_detect_repository (self, mock_detect, mock_commit):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
         
        committer.main(['command', 'message'])
        
        self.assertEquals(call(), mock_detect.call_args)
        
    @patch('committer.handler.commit', return_value=0)    
    @patch('committer.repositories.detect')
    def test_should_commit_use_first_argument_as_message (self, mock_detect, mock_commit):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        actual_return_code = committer.main(['command', 'message'])
        
        self.assertEquals(call(mock_repository, 'message'), mock_commit.call_args)
        self.assertEquals(0, actual_return_code)

    @patch('committer.handler.commit', return_value=0)    
    @patch('committer.repositories.detect')
    def test_should_commit_and_increment_when_second_argument_is_plus_plus (self, mock_detect, mock_commit):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        
        actual_return_code = committer.main(['command', 'message', '++'])
        
        self.assertEquals(call(mock_repository, 'message', increment=True), mock_commit.call_args)
        self.assertEquals(0, actual_return_code)
    
    @patch('committer.repositories.detect')
    @patch('committer.error', return_value=2)
    def test_should_exit_when_no_repository_could_be_detected (self, mock_error, mock_detect):
        mock_detect.return_value = []
        
        actual_return_code = committer.main(['command', 'message', '++'])
        
        self.assertEquals(2, actual_return_code)
        
    @patch('committer.repositories.detect')
    @patch('committer.error', return_value=3)
    def test_should_exit_when_more_than_one_repository_have_been_detected (self, mock_error, mock_detect):
        mock_detect.return_value = [self.create_mock_repository(), self.create_mock_repository()]
        
        actual_return_code = committer.main(['command', 'message', '++'])
        
        self.assertEquals(3, actual_return_code)
