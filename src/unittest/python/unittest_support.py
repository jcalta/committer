import unittest

from mock import Mock


class TestCase (unittest.TestCase):
    def create_mock_repository (self):
        mock_repository         = Mock()
        mock_repository.COMMAND = 'repository-command'
        mock_repository.NAME    = 'mocked-repository'
        return mock_repository    