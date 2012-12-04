import unittest

from mock import Mock


class TestCase (unittest.TestCase):
    def create_mock_vcs_client (self):
        mock_vcs_client = Mock()
        mock_vcs_client.COMMAND = 'mock-vcs-command'
        mock_vcs_client.NAME = 'MockRepository'
        return mock_vcs_client    