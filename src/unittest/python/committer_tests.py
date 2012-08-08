from mock import call, patch

import unittest_support


from committer import commit, errors, update


class CommitTests (unittest_support.TestCase):
    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_check_that_repository_is_executable (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        mock_repository.is_executable.return_value = True 
        
        commit(['/usr/local/bin/commit', 'message'], 'usage information')
        
        self.assertEquals(call(), mock_repository.is_executable.call_args)


    @patch('sys.stdout')
    @patch('sys.stderr')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_return_with_error_when_repository_command_is_not_executable (self, mock_detect, mock_incrementor, mock_stderr, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        mock_repository.is_executable.return_value = False 
        
        self.assertRaises(errors.NotExecutableException, commit, ['/usr/local/bin/commit', 'message'], 'usage information')
        

    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_detect_repository (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
         
        commit(['/usr/local/bin/commit', 'message'], 'usage information')
        
        self.assertEquals(call(), mock_detect.call_args)


    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_return_with_zero (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        
        commit(['/usr/local/bin/commit', 'message'], 'usage information')


    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_call_update_on_repository (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        
        commit(['/usr/local/bin/commit', 'message'], 'usage information')
        
        self.assertEquals(call(), mock_repository.update.call_args)


    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_commit_using_first_argument_as_message (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        
        commit(['/usr/local/bin/commit', 'message'], 'usage information')
        
        self.assertEquals(call('message'), mock_repository.commit.call_args)


    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_increment_when_second_argument_is_plus_plus (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        
        commit(['/usr/local/bin/commit', 'message', '++'], 'usage information')
        
        self.assertEquals(call(), mock_incrementor.increment_version.call_args)


    @patch('sys.stdout')
    @patch('sys.stderr')
    @patch('committer.repositories.detect')
    def test_should_exit_when_no_repository_could_be_detected (self, mock_detect, mock_stderr, mock_stdout):
        mock_detect.return_value = []
        
        self.assertRaises(errors.NoRepositoryDetectedException, commit, ['/usr/local/bin/commit', 'message', '++'], 'usage information')
        

    @patch('sys.stdout')
    @patch('sys.stderr')
    @patch('committer.repositories.detect')
    def test_should_exit_when_more_than_one_repository_have_been_detected (self, mock_detect, mock_stderr, mock_stdout):
        mock_detect.return_value = [self.create_mock_repository(), self.create_mock_repository()]
        
        self.assertRaises(errors.TooManyRepositoriesException, commit, ['/usr/local/bin/commit', 'message', '++'], 'usage information')


class UpdateTests (unittest_support.TestCase):
    @patch('sys.stdout')
    @patch('committer.repositories.detect')
    def test_should_return_with_zero_when_updating (self, mock_detect, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]

        update(['/usr/local/bin/update'], 'usage information')
        

    @patch('sys.stdout')
    @patch('committer.incrementor')    
    @patch('committer.repositories.detect')
    def test_should_update_on_update (self, mock_detect, mock_incrementor, mock_stdout):
        mock_repository = self.create_mock_repository()
        mock_detect.return_value = [mock_repository]
        
        update(['/usr/local/bin/update'], 'usage information')
        
        self.assertEquals(call(), mock_repository.update.call_args)
