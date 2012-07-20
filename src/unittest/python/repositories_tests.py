import unittest

from mock import patch

from committer import repositories

class RepositoriesTests (unittest.TestCase):
    @patch('committer.repositories.git')
    def test_should_return_new_git_object (self, mock_git):
        actual_repository = repositories.detect()
        
        self.assertEquals(mock_git, actual_repository)
