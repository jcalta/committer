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


    @patch('sys.stdout')
    @patch('committer.error', return_value=5)
    def test_should_exit_when_no_arguments_given (self, mock_error, mock_stdout):
        actual_return_code = committer.main(['commit'])
        
        self.assertEquals(5, actual_return_code)


    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_detect_repository (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
         
        committer.main(['/usr/local/bin/commit', 'message'])
        
        self.assertEquals(call(), mock_detect.call_args)


    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_return_with_zero (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        
        actual_return_code = committer.main(['/usr/local/bin/commit', 'message'])
        
        self.assertEquals(0, actual_return_code)


    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_call_update_on_repository (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        
        actual_return_code = committer.main(['/usr/local/bin/commit', 'message'])
        
        self.assertEquals(call(), mock_repository.update.call_args)


    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_commit_using_first_argument_as_message (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        
        actual_return_code = committer.main(['/usr/local/bin/commit', 'message'])
        
        self.assertEquals(call('message'), mock_repository.commit.call_args)
        self.assertEquals(0, actual_return_code)


    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_not_commit_when_called_via_update (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        
        actual_return_code = committer.main(['/usr/local/bin/update', 'message'])
        
        self.assertEquals(None, mock_repository.commit.call_args)
        self.assertEquals(0, actual_return_code)


    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_increment_when_second_argument_is_plus_plus (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        
        actual_return_code = committer.main(['/usr/local/bin/commit', 'message', '++'])
        
        self.assertEquals(call(), mock_incrementor.increment_version.call_args)
        self.assertEquals(0, actual_return_code)


    @patch('sys.stdout')
    @patch('committer.repositories.detect')
    @patch('committer.error', return_value=2)
    def test_should_exit_when_no_repository_could_be_detected (self, mock_error, mock_detect, mock_stdout):
        mock_detect.return_value = []
        
        actual_return_code = committer.main(['/usr/local/bin/commit', 'message', '++'])
        
        self.assertEquals(2, actual_return_code)


    @patch('sys.stdout')
    @patch('committer.repositories.detect')
    @patch('committer.error', return_value=3)
    def test_should_exit_when_more_than_one_repository_have_been_detected (self, mock_error, mock_detect, mock_stdout):
        mock_detect.return_value = [self.create_mock_repository(), self.create_mock_repository()]
        
        actual_return_code = committer.main(['/usr/local/bin/commit', 'message', '++'])
        
        self.assertEquals(3, actual_return_code)
