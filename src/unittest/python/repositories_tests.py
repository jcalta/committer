from mock import call, patch

import unittest_support

from committer import repositories

class RepositoriesTests (unittest_support.TestCase):
    def test_should_find_mercurial_repository (self):
        actual_repositories = repositories.find()
        actual_count_of_repositories = len(actual_repositories)
        
        self.assertEquals(2, actual_count_of_repositories)
    
    def test_should_find_git_repository (self):
        actual_repositories = repositories.find()
        
        self.assertTrue(repositories.git in actual_repositories)
    
    def test_should_find_mercurial_repository (self):
        actual_repositories = repositories.find()
        
        self.assertTrue(repositories.mercurial in actual_repositories)
    
    @patch('committer.repositories.find')
    def test_should_return_repository_module_when_detect_returns_true (self, mock_find):
        mock_repository = self.create_mock_repository()
        mock_repository.detect.return_value = True
        mock_find.return_value = [mock_repository]
        
        actual_detected_repositories = repositories.detect()
        
        self.assertEquals([mock_repository], actual_detected_repositories)
        self.assertEquals(call(), mock_repository.detect.call_args)

    @patch('committer.repositories.find')
    def test_should_return_no_repository_module_when_detection_fails (self, mock_find):
        mock_repository = self.create_mock_repository()
        mock_repository.detect.return_value = False
        mock_find.return_value = [mock_repository]
        
        actual_detected_repositories = repositories.detect()
        
        self.assertEquals([], actual_detected_repositories)
        self.assertEquals(call(), mock_repository.detect.call_args)
