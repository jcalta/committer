import unittest

from mock import call, patch

from committer import repositories

class RepositoriesTests (unittest.TestCase):
    def test_should_contain_git_repository (self):
        actual_repositories = repositories.find()
        
        self.assertTrue(repositories.git in actual_repositories)
    
    @patch('committer.repositories.git')
    def test_should_return_git_module (self, mock_git):
        mock_git.detect.return_value = True
        
        actual_repository = repositories.detect()
        
        self.assertEquals(mock_git, actual_repository)
        self.assertEquals(call(), mock_git.detect.call_args)

    @patch('sys.exit')
    @patch('committer.repositories.git')
    def test_should_exit_if_no_repository_detected (self, mock_git, mock_exit):
        mock_git.detect.return_value = False
        
        repositories.detect()
        
        self.assertEquals(call(), mock_git.detect.call_args)
        self.assertEquals(call(1), mock_exit.call_args)
